from typing import TypedDict, Any

from crowdin_api.api_resources.enums import PatchOperation


class ApprovalBatchOpPatchRequest(TypedDict):
    op: PatchOperation
    path: str
    value: Any


class TranslationBatchOpPatchRequest(TypedDict):
    op: PatchOperation
    path: str
    value: Any
