from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.tasks.enums import (
    TaskOperationPatchPath,
    VendorTaskOperationPatchPath,
)
from crowdin_api.typing import TypedDict


class CrowdinTaskAssignee(TypedDict, total=False):
    id: int
    wordsCount: int


class TaskPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TaskOperationPatchPath


class VendorPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: VendorTaskOperationPatchPath
