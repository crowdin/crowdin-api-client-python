from typing import List, Optional, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import (
    BranchPatchPath,
    DirectoryPatchPath,
    EscapeQuotes,
    FilePatchPath,
    FileUpdateOption,
)
from crowdin_api.typing import TypedDict


class BranchPatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: Union[PatchOperation, str]
    path: BranchPatchPath


class DirectoryPatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: Union[PatchOperation, str]
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
    translatableElements: List[str]


class OtherImportOptions(TypedDict):
    contentSegmentation: bool


class GeneralExportOptions(TypedDict):
    exportPattern: str


class PropertyExportOptions:
    escapeQuotes: EscapeQuotes
    exportPattern: str


class ReplaceFileFromStorageRequest(TypedDict):
    storageId: int
    updateOption: Optional[FileUpdateOption]
    importOptions: Optional[
        Union[SpreadsheetImportOptions, XmlImportOptions, OtherImportOptions]
    ]
    exportOptions: Optional[Union[GeneralExportOptions, PropertyExportOptions]]
    attachLabelIds: Optional[List[int]]
    detachLabelIds: Optional[List[int]]


class FilePatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: Union[PatchOperation, str]
    path: FilePatchPath
