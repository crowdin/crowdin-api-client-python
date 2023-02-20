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


class Scheme(TypedDict, total=False):
    identifier: int
    sourcePhrase: int


class SpreadsheetImportOptions(TypedDict):
    firstLineContainsHeader: bool
    importTranslations: bool
    scheme: Scheme
    srxStorageId: int


class XmlImportOptions(TypedDict):
    translateContent: bool
    translateAttributes: bool
    contentSegmentation: bool
    translatableElements: Iterable[str]


class DocxFileImportOptions(TypedDict):
    cleanTagsAggressively: bool
    translateHiddenText: bool
    translateHyperlinkUrls: bool
    translateHiddenRowsAndColumns: bool
    importNotes: bool
    importHiddenSlides: bool
    contentSegmentation: bool
    srxStorageId: int


class OtherImportOptions(TypedDict):
    contentSegmentation: bool
    srxStorageId: int


class GeneralExportOptions(TypedDict):
    exportPattern: str


class PropertyExportOptions:
    escapeQuotes: EscapeQuotes
    exportPattern: str


class FilePatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: FilePatchPath
