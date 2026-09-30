from typing import Any, Dict, Iterable, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import (
    BranchPatchPath,
    DirectoryPatchPath,
    EscapeQuotes,
    EscapeSpecialCharacters,
    ExportQuotes,
    FilePatchPath,
    FrontMatterQuotes,
    MarkdownMarker,
    TableColumnWidth,
    UnorderedListBullet,
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
    none: int
    identifier: int
    sourcePhrase: int
    sourceOrTranslation: int
    translation: int
    context: int
    maxLength: int
    translatable: int
    labels: int


class SpreadsheetImportOptions(TypedDict, total=False):
    firstLineContainsHeader: bool
    importHiddenSheets: bool
    importHiddenRows: bool
    importEqSuggestions: bool
    autoApproveImported: bool
    translateHidden: bool
    addToTm: bool
    contentSegmentation: bool
    srxStorageId: int
    importTranslations: bool
    scheme: Scheme


class XmlImportOptions(TypedDict, total=False):
    translateContent: bool
    translateAttributes: bool
    inlineTags: Iterable[str]
    contentSegmentation: bool
    translatableElements: Iterable[str]
    srxStorageId: int


class WebXmlFileImportOptions(TypedDict, total=False):
    inlineTags: Iterable[str]
    hideAttributeValues: bool
    contentSegmentation: bool
    srxStorageId: int


class DocxFileImportOptions(TypedDict, total=False):
    cleanTagsAggressively: bool
    translateHiddenText: bool
    translateHyperlinkUrls: bool
    translateHiddenRowsAndColumns: bool
    importNotes: bool
    importHiddenSlides: bool
    contentSegmentation: bool
    srxStorageId: int
    translateDocProperties: bool
    translateComments: bool
    ignoreWhitespaceStyles: bool
    addTabAsCharacter: bool
    addLineSeparatorAsCharacter: bool
    lineSeparatorReplacement: str
    replaceNoBreakHyphenTag: bool
    ignoreSoftHyphenTag: bool
    complexFieldDefinitionsToExtract: Iterable[str]
    translateWordHeadersFooters: bool
    translateWordGraphicName: bool
    translateWordGraphicDescription: bool
    ignoreWordFontColors: bool
    wordFontColorsMinIgnoranceThreshold: str
    wordFontColorsMaxIgnoranceThreshold: str
    excludeWordStyles: Iterable[str]
    translateWordInExcludeStyleMode: bool
    wordHighlightColors: Iterable[str]
    translateWordInExcludeHighlightMode: bool
    translateWordExcludeColors: bool
    wordExcludedColors: Iterable[str]
    translateExcelCellsCopied: bool
    translateExcelSheetNames: bool
    excelExcludedColors: Iterable[str]
    translateExcelDiagramData: bool
    translateExcelDrawings: bool


class VsdxFileImportOptions(TypedDict, total=False):
    cleanTagsAggressively: bool
    translateHyperlinkUrls: bool
    contentSegmentation: bool
    srxStorageId: int


class IdmlFileImportOptions(TypedDict, total=False):
    inlineHyperlinkText: bool
    contentSegmentation: bool
    srxStorageId: int


class OtherImportOptions(TypedDict, total=False):
    contentSegmentation: bool
    srxStorageId: int


class HtmlFileImportOptions(TypedDict, total=False):
    excludedElements: Iterable[str]
    contentSegmentation: bool
    inlineTags: Iterable[str]
    srxStorageId: int


class HtmlWithFrontMatterFileImportOptions(HtmlFileImportOptions, total=False):
    excludedFrontMatterElements: Iterable[str]


class MdFileImportOptions(TypedDict, total=False):
    excludedFrontMatterElements: Iterable[str]
    excludeCodeBlocks: bool
    inlineTags: Iterable[str]
    contentSegmentation: bool
    srxStorageId: int


class MdxV1FileImportOptions(TypedDict, total=False):
    excludedFrontMatterElements: Iterable[str]
    excludeCodeBlocks: bool
    contentSegmentation: bool
    srxStorageId: int


class MdxV2FileImportOptions(TypedDict, total=False):
    excludedFrontMatterElements: Iterable[str]
    excludeCodeBlocks: bool
    contentSegmentation: bool
    srxStorageId: int


class StringCatalogFileImportOptions(TypedDict, total=False):
    importKeyAsSource: bool
    importTranslations: bool


class AdocFileImportOptions(TypedDict, total=False):
    excludeIncludeDirectives: bool


class VdfFileImportOptions(TypedDict, total=False):
    convertIcu: bool
    addGenderArgument: bool


FileImportOptions = Union[
    SpreadsheetImportOptions,
    XmlImportOptions,
    WebXmlFileImportOptions,
    DocxFileImportOptions,
    VsdxFileImportOptions,
    IdmlFileImportOptions,
    HtmlFileImportOptions,
    HtmlWithFrontMatterFileImportOptions,
    MdFileImportOptions,
    MdxV1FileImportOptions,
    MdxV2FileImportOptions,
    StringCatalogFileImportOptions,
    AdocFileImportOptions,
    VdfFileImportOptions,
    OtherImportOptions,
]


class GeneralExportOptions(TypedDict, total=False):
    exportPattern: str


class PropertyExportOptions(GeneralExportOptions, total=False):
    escapeQuotes: EscapeQuotes
    escapeSpecialCharacters: EscapeSpecialCharacters


class JavascriptExportOptions(GeneralExportOptions, total=False):
    exportQuotes: ExportQuotes


class MdxFileExportOptions(GeneralExportOptions, total=False):
    strongMarker: MarkdownMarker
    emphasisMarker: MarkdownMarker
    unorderedListBullet: UnorderedListBullet
    tableColumnWidth: TableColumnWidth


class MdFileExportOptions(MdxFileExportOptions, total=False):
    frontMatterQuotes: FrontMatterQuotes


class DocxFileExportOptions(GeneralExportOptions, total=False):
    allowWordStyleOptimization: bool
    translateExcelExcludeColors: bool


FileExportOptions = Union[
    GeneralExportOptions,
    PropertyExportOptions,
    JavascriptExportOptions,
    MdFileExportOptions,
    MdxFileExportOptions,
    DocxFileExportOptions,
]

# Enterprise only. Keys get via List Fields.
FileFields = Dict[str, Union[str, int, bool, Iterable[str]]]


class FilePatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: Union[FilePatchPath, str]
