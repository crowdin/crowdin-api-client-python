from typing import TypedDict, Optional, Any

from crowdin_api.api_resources.branches.enums import EditBranchPatchPath
from crowdin_api.api_resources.enums import PatchOperation


class CloneBranchRequest(TypedDict):
    name: str
    title: Optional[str]


class AddBranchRequest(TypedDict):
    name: str
    title: Optional[str]


class EditBranchPatch(TypedDict):
    op: PatchOperation
    path: EditBranchPatchPath
    value: Any


class MergeBranchRequest(TypedDict):
    deleteAfterMerge: Optional[bool]
    sourceBranchId: int
    dryRun: Optional[bool]
