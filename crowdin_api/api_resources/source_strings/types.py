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


class UploadStringsSpreadsheetScheme(TypedDict, total=False):
    """
    Column mapping (numbering starts at 0). Language identifiers (e.g. "en", "de") may also be
    used as keys with a column number as a value.
    """

    none: int
    identifier: int
    sourcePhrase: int
    sourceOrTranslation: int
    translation: int
    context: int
    translatable: int


class UploadStringsSpreadsheetImportOptions(TypedDict, total=False):
    firstLineContainsHeader: bool
    importHiddenSheets: bool
    contentSegmentation: bool
    srxStorageId: int
    scheme: UploadStringsSpreadsheetScheme


class UploadStringsStringCatalogImportOptions(TypedDict, total=False):
    importKeyAsSource: bool
    importTranslations: bool


class UploadStringsOtherImportOptions(TypedDict, total=False):
    contentSegmentation: bool
    srxStorageId: int


UploadStringsImportOptions = Union[
    UploadStringsSpreadsheetImportOptions,
    UploadStringsStringCatalogImportOptions,
    UploadStringsOtherImportOptions,
]
