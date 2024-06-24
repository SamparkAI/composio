"""
App enums.
"""

from composio.client.enums.base import APPS_CACHE, AppData, _AnnotatedEnum, enum


@enum
class App(_AnnotatedEnum[AppData], path=APPS_CACHE):
    """Class to represent `App` entity."""

    APIFY: "App"
    ASANA: "App"
    ATTIO: "App"
    BREVO: "App"
    CLICKUP: "App"
    CODEINTERPRETER: "App"
    COMPOSIO: "App"
    DISCORD: "App"
    DROPBOX: "App"
    ELEVENLABS: "App"
    EXA: "App"
    FIGMA: "App"
    FILEMANAGER: "App"
    FIRECRAWL: "App"
    GITHUB: "App"
    GMAIL: "App"
    GOOGLECALENDAR: "App"
    GOOGLEDOCS: "App"
    GOOGLEDRIVE: "App"
    GOOGLEMEET: "App"
    GOOGLESHEETS: "App"
    GOOGLETASKS: "App"
    HACKERNEWS: "App"
    HEROKU: "App"
    INDUCEDAI: "App"
    LINEAR: "App"
    LISTENNOTES: "App"
    MULTIONAI: "App"
    NASA: "App"
    NOTION: "App"
    OKTA: "App"
    PAGERDUTY: "App"
    PERPLEXITYAI: "App"
    SCHEDULER: "App"
    SERPAPI: "App"
    SLACK: "App"
    SLACKBOT: "App"
    SNOWFLAKE: "App"
    SOUNDCLOUD: "App"
    SPLITWISE: "App"
    SPOTIFY: "App"
    STRAVA: "App"
    TASKADE: "App"
    TAVILY: "App"
    TRELLO: "App"
    TWILIO: "App"
    TYPEFORM: "App"
    WEATHERMAP: "App"
    WHATSAPP: "App"
    WORKABLE: "App"
    YOUSEARCH: "App"
    YOUTUBE: "App"
    ZENDESK: "App"
    ZOOM: "App"
    MATHEMATICAL: "App"
    LOCALWORKSPACE: "App"
    CMDMANAGERTOOL: "App"
    HISTORYKEEPER: "App"
    RAGTOOL: "App"
    WEBTOOL: "App"
    GREPTILE: "App"
    SUBMITPATCHTOOL: "App"

    @property
    def is_local(self) -> bool:
        """The tool is local if set to `True`"""
        return self.load().is_local

    @property
    def name(self) -> str:
        """Name of the app."""
        return self.load().name