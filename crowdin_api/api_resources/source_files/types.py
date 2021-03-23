from typing import Any, Iterable

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import (
    BranchPatchPath,
    DirectoryPatchPath,
    EscapeQuotes,
    FilePatchPath,
)
from crowdin_api.typing import TypedDict


class BranchPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: BranchPatchPath


class DirectoryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: DirectoryPatchPath


Scheme = TypedDict("Scheme", {"identifier": int, "sourcePhrase": int}, total=False)


class SpreadsheetImportOptions(TypedDict):
    firstLineContainsHeader: bool
    importTranslations: bool
    scheme: Scheme


class XmlImportOptions(TypedDict):
    translateContent: bool
    translateAttributes: bool
    contentSegmentation: bool
    translatableElements: Iterable[str]


class OtherImportOptions(TypedDict):
    contentSegmentation: bool


class GeneralExportOptions(TypedDict):
    exportPattern: str


class PropertyExportOptions:
    escapeQuotes: EscapeQuotes
    exportPattern: str


class FilePatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: FilePatchPath
