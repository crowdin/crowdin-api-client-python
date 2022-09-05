from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.groups.enums import GroupPatchPath
from crowdin_api.typing import TypedDict


class GroupPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: GroupPatchPath
