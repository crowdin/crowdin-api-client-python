from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.tasks.enums import (
    TaskOperationPatchPath,
    VendorTaskOperationPatchPath,
)
from crowdin_api.typing import TypedDict

CrowdinTaskAssignee = TypedDict(
    "CrowdinTaskAssignee",
    {"id": int, "wordsCount": int},
    total=False,
)


class TaskPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TaskOperationPatchPath


class VendorPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: VendorTaskOperationPatchPath
