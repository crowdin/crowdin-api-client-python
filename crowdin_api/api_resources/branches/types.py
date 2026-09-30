from typing import Optional, Any

from crowdin_api.api_resources.branches.enums import EditBranchPatchPath
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import Priority
from crowdin_api.typing import TypedDict


class _CloneBranchRequestRequired(TypedDict):
    name: str


class CloneBranchRequest(_CloneBranchRequestRequired, total=False):
    """String-based projects only."""

    title: Optional[str]
    isProtected: Optional[bool]


class _AddBranchRequestRequired(TypedDict):
    name: str


class AddBranchRequest(_AddBranchRequestRequired, total=False):
    """
    `exportPattern` and `priority` are for file-based projects only,
    `isProtected` is for string-based projects only.
    """

    title: Optional[str]
    exportPattern: Optional[str]
    priority: Optional[Priority]
    isProtected: Optional[bool]


class EditBranchPatch(TypedDict):
    op: PatchOperation
    path: EditBranchPatchPath
    value: Any


class _MergeBranchRequestRequired(TypedDict):
    sourceBranchId: int


class MergeBranchRequest(_MergeBranchRequestRequired, total=False):
    """String-based projects only."""

    deleteAfterMerge: Optional[bool]
    dryRun: Optional[bool]
    acceptSourceChanges: Optional[bool]
