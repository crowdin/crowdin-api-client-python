from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import ProjectPatchPath
from crowdin_api.typing import TypedDict


class ProjectPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: ProjectPatchPath
