from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.project_placeholders.enums import ProjectPlaceholderPatchPath
from crowdin_api.typing import TypedDict


class ProjectPlaceholderPatchRequest(TypedDict):
    """
    `op` accepts `replace` or `test` only.
    """

    op: PatchOperation
    path: ProjectPlaceholderPatchPath
    value: Any
