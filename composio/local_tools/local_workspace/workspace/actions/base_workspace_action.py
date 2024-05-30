from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, Field

from composio.local_tools.action import Action
from composio.local_tools.local_workspace.commons.get_logger import get_logger
from composio.local_tools.local_workspace.commons.history_processor import (
    HistoryProcessor,
)
from composio.local_tools.local_workspace.commons.local_docker_workspace import (
    WorkspaceManagerFactory,
)


logger = get_logger()


class BaseWorkspaceRequest(BaseModel):
    pass


class BaseWorkspaceResponse(BaseModel):
    pass


class BaseWorkspaceAction(Action, ABC):
    """
    Base class for all Workspace actions
    """

    _display_name = ""
    _request_schema = BaseWorkspaceRequest
    _response_schema = BaseWorkspaceResponse
    _tags = ["workspace"]
    _tool_name = "localworkspace"
    workspace_factory: Optional[WorkspaceManagerFactory] = None
    history_processor: Optional[HistoryProcessor] = None

    def __init__(self):
        super().__init__()
        self.args = None
        self.workspace_id = ""
        self.container_name = ""
        self.image_name = ""
        self.container_process = None
        self.parent_pids = []
        self.container_obj = None
        self.return_code = None
        self.logger = logger
        self.config = None
        self.config_file_path = None

    def set_workspace_and_history(
        self,
        workspace_factory: WorkspaceManagerFactory,
        history_processor: HistoryProcessor,
    ):
        self.workspace_factory = workspace_factory
        self.history_processor = history_processor

    @abstractmethod
    def execute(
        self, request_data: BaseWorkspaceRequest, authorisation_data: dict
    ) -> BaseWorkspaceResponse:
        pass