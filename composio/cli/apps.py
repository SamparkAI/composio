"""
Apps manager for Composio SDK.

Usage:
    composio apps [command] [options]
"""

import typing as t

import click

from composio.cli.context import Context, pass_context
from composio.client import ActionModel, AppModel, TriggerModel, enums
from composio.exceptions import ComposioSDKError


MODULE_TEMPLATE = """\"\"\"
Helper Enum classes.

- TODO: Replace Enums with something lightweight
\"\"\"

from enum import Enum


{tag_enum}

{app_enum}

{action_enum}

{trigger_enum}
"""

TAG_ENUM_TEMPLATE = """class Tag(tuple, Enum):
    \"\"\"App tags.\"\"\"

    @property
    def name(self) -> str:
        \"\"\"Returns trigger name.\"\"\"
        return self.value[0]

    IMPORTANT = ("default", "important")
{tags}
"""

APP_ENUM_TEMPLATE = """class App(str, Enum):
    \"\"\"Composio App.\"\"\"

{apps}
"""

ACTION_ENUM_TEMPLATE = """class Action(tuple, Enum):
    \"\"\"App action.\"\"\"

    @property
    def app(self) -> str:
        \"\"\"Name of the app where this actions belongs.\"\"\"
        return self.value[0]

    @property
    def action(self) -> str:
        \"\"\"Name of the action.\"\"\"
        return self.value[1]

    @property
    def no_auth(self) -> bool:
        \"\"\"Name of the action.\"\"\"
        return self.value[2]

    @classmethod
    def from_app(cls, name: str) -> "Action":
        \"\"\"Create Action type enum from app name.\"\"\"
        for action in cls:
            if name == action.app:
                return action
        raise ValueError(f"No action type found for name `{{name}}`")

    @classmethod
    def from_action(cls, name: str) -> "Action":
        \"\"\"Create Action type enum from action name.\"\"\"
        for action in cls:
            if name == action.action:
                return action
        raise ValueError(f"No action type found for name `{{name}}`")

    @classmethod
    def from_app_and_action(cls, app: str, name: str) -> "Action":
        \"\"\"From name and action params.\"\"\"
        for action in cls:
            if app == action.app and name == action.action:
                return action
        raise ValueError("No action type found for app " f"`{{app}}` and action `{{name}}`")

{actions}
"""

TRIGGER_ENUM_TEMPLATE = """class Trigger(tuple, Enum):
    \"\"\"App trigger.\"\"\"

    @property
    def app(self) -> str:
        \"\"\"App name.\"\"\"
        return self.value[0]

    @property
    def event(self) -> str:
        \"\"\"Event name.\"\"\"
        return self.value[1]

{triggers}
"""


@click.group(name="apps", invoke_without_command=True)
@click.option(
    "--enabled",
    is_flag=True,
    default=False,
    help="Only show apps which are enabled",
)
@pass_context
def _apps(context: Context, enabled: bool = False) -> None:
    """Manage composio apps"""
    if context.click_ctx.invoked_subcommand:
        return

    try:
        apps = context.client.apps.get()
        if enabled:
            apps = [app for app in apps if app.enabled]
            context.console.print("[green]Showing apps which are enabled[/green]")
        else:
            context.console.print("[green]Showing all apps[/green]")
        for app in apps:
            context.console.print(f"• {app.name}")
    except ComposioSDKError as e:
        raise click.ClickException(message=e.message) from e


@_apps.command(name="update")
@pass_context
def _update(context: Context) -> None:
    """Updates local Apps database."""
    try:
        apps = sorted(
            context.client.apps.get(),
            key=lambda x: x.key,
        )
        actions = sorted(
            context.client.actions.get(allow_all=True),
            key=lambda x: x.appKey,
        )
        triggers = sorted(
            context.client.triggers.get(),
            key=lambda x: x.appKey,
        )
        enum_module = MODULE_TEMPLATE.format(
            tag_enum=_get_tag_enum(apps=apps, actions=actions),
            app_enum=_get_app_enum(apps=apps),
            action_enum=_get_action_enum(apps=apps, actions=actions),
            trigger_enum=_get_trigger_enum(apps=apps, triggers=triggers),
        )
        with open(enums.__file__, "w", encoding="utf-8") as file:
            file.write(enum_module)
    except ComposioSDKError as e:
        raise click.ClickException(message=e.message) from e


def _get_tag_enum(apps: t.List[AppModel], actions: t.List[ActionModel]) -> str:
    """Create Tag enum class."""
    tag_map: t.Dict[str, t.Set[str]] = {}
    for app in apps:
        app_key = app.key
        app_actions = [action for action in actions if action.appKey == app_key]
        for action in app_actions:
            if app_key not in tag_map:
                tag_map[app_key] = set()
            tag_map[app_key].update(action.tags or [])

    tag_enums = ""
    for app_key, tags in tag_map.items():
        for tag in tags:
            tag_name = _get_enum_key(f"{app_key}_{tag}")
            tag_enums += f'    {tag_name} = ("{app_key}", "{tag}")\n'
    tag_enums += "\n"
    return TAG_ENUM_TEMPLATE.format(tags=tag_enums)


def _get_app_enum(apps: t.List[AppModel]) -> str:
    """Create App enum class."""
    app_enums = ""
    for app in apps:
        app_name = app.key.upper().replace(" ", "_").replace("-", "_")
        app_enums += f'    {_get_enum_key(app_name)} = "{app.key}"\n'
    return APP_ENUM_TEMPLATE.format(apps=app_enums)


def _get_action_enum(apps: t.List[AppModel], actions: t.List[ActionModel]) -> str:
    """Get Action enum."""
    action_enums = ""
    for app in apps:
        app_actions = [action for action in actions if action.appKey == app.key]
        for action in app_actions:
            enum_name = f"{_get_enum_key(action.name)}"
            enum_value = f'("{app.key}", "{action.name}", {app.no_auth})'
            action_enums += f"    {enum_name} = {enum_value}\n"
    return ACTION_ENUM_TEMPLATE.format(actions=action_enums)


def _get_trigger_enum(
    apps: t.List[AppModel],
    triggers: t.List[TriggerModel],
) -> str:
    """Get Trigger enum."""
    trigger_enums = ""
    for app in apps:
        app_triggers = [trigger for trigger in triggers if trigger.appKey == app.key]
        for trigger in app_triggers:
            enum_name = f"{_get_enum_key(app.key.upper())}_{_get_enum_key(trigger.display_name)}"
            enum_value = f'("{app.key}", "{trigger.name}")'
            trigger_enums += f"    {enum_name} = {enum_value}\n"
    return TRIGGER_ENUM_TEMPLATE.format(triggers=trigger_enums)


def _get_enum_key(name: str) -> str:
    characters_to_replace = [" ", "-", "/", "(", ")", "\\", ":", '"', "'", "."]
    for char in characters_to_replace:
        name = name.replace(char, "_")
    return name.upper()