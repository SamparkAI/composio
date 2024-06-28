import typing as t
from uuid import uuid4

from composio.workspace import DockerWorkspace, E2BWorkspace, LocalDockerArgumentsModel
from composio.workspace.base_workspace import Workspace
from composio.workspace.workspace_clients import DockerIoClient, E2BClient, WorkspaceType

import composio.workspace.constants as workspace_const

KEY_WORKSPACE_MANAGER = "workspace"
KEY_CONTAINER_NAME = "container_name"
KEY_PARENT_PIDS = "parent_pids"
KEY_IMAGE_NAME = "image_name"
KEY_WORKSPACE_ID = "workspace_id"
KEY_WORKSPACE_TYPE = "type"


class WorkspaceFactory:
    _instance = None  # Singleton instance
    docker_client = None
    e2b_client = None
    _registry = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkspaceFactory, cls).__new__(cls)
            cls._instance.docker_client = DockerIoClient()
            cls._instance.e2b_client = E2BClient()
            cls._instance._registry = {}
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the WorkspaceFactory."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_workspace(self, workspace_type: WorkspaceType,
                         local_docker_args: LocalDockerArgumentsModel,
                         **kwargs) -> str:
        if workspace_type == WorkspaceType.DOCKER:
            workspace = DockerWorkspace(local_docker_args.image_name, self.docker_client, local_docker_args)
            workspace.setup(env=workspace_const.get_default_docker_env())
            workspace_id = str(uuid4())
            self._registry[workspace_id] = {
                KEY_WORKSPACE_MANAGER: workspace,
                KEY_CONTAINER_NAME: workspace.container_name,
                KEY_PARENT_PIDS: workspace.parent_pids,
                KEY_IMAGE_NAME: local_docker_args.image_name,
                KEY_WORKSPACE_TYPE: WorkspaceType.DOCKER,
            }
            return workspace_id
        elif workspace_type == WorkspaceType.E2B:
            workspace = E2BWorkspace(None, self.e2b_client)
            workspace_id = str(uuid4())
            self._registry[workspace_id] = {
                KEY_WORKSPACE_MANAGER: workspace,
                KEY_WORKSPACE_TYPE: WorkspaceType.DOCKER,
            }
        else:
            raise ValueError(f"Unsupported workspace type: {workspace_type}")

        return None

    def get_registered_manager(self, workspace_id: str) -> t.Optional[t.Dict[str, t.Any]]:
        return self._registry.get(workspace_id)

    def get_workspace_by_id(self, workspace_id: str) -> Workspace:
        workspace_meta = self._registry.get(workspace_id)
        workspace = workspace_meta[KEY_WORKSPACE_MANAGER]
        return workspace

    def remove_workspace_manager(self, workspace_id: str) -> None:
        if workspace_id in self._registry:
            del self._registry[workspace_id]

    def list_workspace_managers(self) -> t.Dict[str, t.Any]:
        return self._registry
