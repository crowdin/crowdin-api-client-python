from typing import Any, Iterable, List, Union, Dict

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    ProjectPatchPath,
    EscapeQuotes,
    EscapeSpecialCharacters,
    ProjectFilePatchPath,
    StringsExporterSettingsPatchPath,
    TmPreTranslateAutoApproveOption,
    TmPreTranslateMinimumMatchRatio,
)
from crowdin_api.typing import TypedDict


class ProjectPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: ProjectPatchPath


class NotificationSettings(TypedDict):
    translatorNewStrings: bool
    managerNewStrings: bool
    managerLanguageCompleted: bool


class QACheckCategories(TypedDict, total=False):
    empty: bool
    size: bool
    tags: bool
    spaces: bool
    variables: bool
    punctuation: bool
    symbolRegister: bool
    specialSymbols: bool
    wrongTranslation: bool
    spellcheck: bool
    icu: bool
    terms: bool
    duplicate: bool
    ftl: bool
    android: bool
    numbers: bool
    ai: bool
    outdated: bool
    mdx: bool
    unifiedPlaceholders: bool


class QAChecksIgnorableCategories(QACheckCategories, total=False):
    pass


class TmPreTranslate(TypedDict, total=False):
    """
    Crowdin only.
    """

    enabled: bool
    autoApproveOption: TmPreTranslateAutoApproveOption
    minimumMatchRatio: TmPreTranslateMinimumMatchRatio


class MtPreTranslateEngineSettings(TypedDict, total=False):
    mtId: int
    languageIds: Iterable[str]


class MtPreTranslate(TypedDict, total=False):
    """
    Crowdin only.
    """

    enabled: bool
    mts: Iterable[MtPreTranslateEngineSettings]


class AiPreTranslatePromptSettings(TypedDict, total=False):
    aiPromptId: int
    languageIds: Iterable[str]


class AiPreTranslate(TypedDict, total=False):
    """
    Crowdin only.
    """

    enabled: bool
    aiPrompts: Iterable[AiPreTranslatePromptSettings]


class WorkflowStepConfig(TypedDict, total=False):
    """
    Keys are Language Identifiers, values are User (`assignees`) or Team (`assignedTeams`) Identifiers.
    """

    assignees: Dict[str, Iterable[int]]
    assignedTeams: Dict[str, Iterable[int]]


class _WorkflowStepSettingsRequired(TypedDict):
    id: int


class WorkflowStepSettings(_WorkflowStepSettingsRequired, total=False):
    """
    Crowdin Enterprise only. Workflow Template Step configuration.

    Use `config` for Translation and Proofreading steps, `vendorId` for vendor steps,
    `mtId` for machine translation steps and `promptId` for AI steps.
    """

    languages: Iterable[str]
    config: WorkflowStepConfig
    vendorId: int
    mtId: int
    promptId: int


class PropertyFileFormatSettings(TypedDict, total=False):
    escapeQuotes: EscapeQuotes
    escapeSpecialCharacters: EscapeSpecialCharacters
    exportPattern: str


class XmlFileFormatSettings(TypedDict, total=False):
    translateContent: bool
    translateAttributes: bool
    translatableElements: Iterable[str]
    contentSegmentation: bool
    srxStorageId: int
    inlineTags: Iterable[str]
    exportPattern: str


class SpecificFileFormatSettings(TypedDict, total=False):
    """
    Includes kind standard file format settings:
        - WebXml file (`inlineTags`)
        - Html file (`inlineTags`, `excludedElements`)
        - Adoc file (`excludeIncludeDirectives`)
        - Android file
        - FmMd file
        - FmHtml file (`inlineTags`, `excludedElements`, `excludedFrontMatterElements`)
        - MadcapFlsnp file
        - Idml file (`inlineHyperlinkText`)
        - Mif file
        - Dita file
        - Arb file
        - Fjs file
        - MacOSX file
        - Chrome file
        - CSV file
        - XLSX file
        - Xliff file
        - Xliff 2.0 file
        - React intl file
    """
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str
    inlineTags: Iterable[str]
    excludedElements: Iterable[str]
    excludedFrontMatterElements: Iterable[str]
    excludeIncludeDirectives: bool
    inlineHyperlinkText: bool


class MdFileFormatSettings(TypedDict, total=False):
    """
    Markdown file format settings.

    Values available:
        - strongMarker, emphasisMarker: "asterisk", "underscore"
        - unorderedListBullet: "asterisks", "plus", "dash"
        - tableColumnWidth: "consolidate", "evenly_distribute_cells"
        - frontMatterQuotes: "auto", "single", "double"
    """
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str
    inlineTags: Iterable[str]
    strongMarker: str
    emphasisMarker: str
    unorderedListBullet: str
    tableColumnWidth: str
    frontMatterQuotes: str


class MdxFileFormatSettings(TypedDict, total=False):
    """
    Mdx v1 / Mdx v2 file format settings.

    Values available:
        - type (Mdx v1 only): "mdx_v1", "mdx_v2"
        - strongMarker, emphasisMarker: "asterisk", "underscore"
        - unorderedListBullet: "asterisks", "plus", "dash"
        - tableColumnWidth: "consolidate", "evenly_distribute_cells"
    """
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str
    type: str
    excludedFrontMatterElements: Iterable[str]
    excludeCodeBlocks: bool
    strongMarker: str
    emphasisMarker: str
    unorderedListBullet: str
    tableColumnWidth: str


class JsonFileFormatSettings(TypedDict, total=False):
    """
    Json file format settings.

    Values available for `type`: "i18next_json", "nestjs_i18n".
    """
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str
    type: str


class JavaScriptFileFormatSettings(TypedDict, total=False):
    """
    JavaScript file format settings.

    Values available for `exportQuotes`: "single", "double".
    """
    exportPattern: str
    exportQuotes: str


class StringCatalogFileFormatSettings(TypedDict, total=False):
    importKeyAsSource: bool
    importTranslations: bool
    exportPattern: str


class VdfFileFormatSettings(TypedDict, total=False):
    convertIcu: bool
    addGenderArgument: bool
    exportPattern: str


class DocxFileFormatSettings(TypedDict, total=False):
    cleanTagsAggressively: bool
    translateHiddenText: bool
    translateHyperlinkUrls: bool
    translateHiddenRowsAndColumns: bool
    importNotes: bool
    importHiddenSlides: bool
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str
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
    allowWordStyleOptimization: bool
    translateExcelExcludeColors: bool


class MediaWikiFileFormatSettings(TypedDict, total=False):
    srxStorageId: int
    exportPattern: str


class TxtFileFormatSettings(TypedDict, total=False):
    srxStorageId: int
    exportPattern: str


class OtherFileFormatSettings(TypedDict, total=False):
    exportPattern: str


class AndroidStringsExporterSettings(TypedDict, total=False):
    convertPlaceholders: bool
    convertLineBreaks: bool
    useCdataForStringsWithTags: bool


class MacOSXStringsExporterSettings(TypedDict, total=False):
    convertPlaceholders: bool
    convertLineBreaks: bool
    exportContext: bool


class XliffStringsExporterSettings(TypedDict, total=False):
    languagePairMapping: Dict[str, str]
    copySourceToEmptyTarget: bool
    exportTranslatorsComment: bool


class StringsExporterSettingsPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: StringsExporterSettingsPatchPath


class ProjectFilePatchRequest(TypedDict):
    value: Union[str, List[str], Dict[str, Any]]
    op: PatchOperation
    path: ProjectFilePatchPath
