from typing import Any, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_strings.enums import (
    SourceStringsPatchPath,
    StringBatchOperations,
    StringBatchOperationsPath,
)
from crowdin_api.typing import TypedDict


class SourceStringsPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: SourceStringsPatchPath


class StringBatchOperationPatchRequest(TypedDict):
    op: StringBatchOperations
    path: StringBatchOperationsPath
    value: Union[str, dict, int, bool]
