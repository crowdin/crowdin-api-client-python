from enum import Enum


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class BranchPatchPath(Enum):
    NAME = "/name"
    TITLE = "/title"
    EXPORT_PATTERN = "/exportPattern"  # file-based projects only
    PRIORITY = "/priority"
    IS_PROTECTED = "/isProtected"  # string-based projects only


class DirectoryPatchPath(Enum):
    BRANCH_ID = "/branchId"
    DIRECTORY_ID = "/directoryId"
    NAME = "/name"
    TITLE = "/title"
    EXPORT_PATTERN = "/exportPattern"
    PRIORITY = "/priority"


class FileType(Enum):
    AUTO = "auto"
    ANDROID = "android"
    MACOSX = "macosx"
    RESX = "resx"
    PROPERTIES = "properties"
    GETTEXT = "gettext"
    YAML = "yaml"
    PHP = "php"
    JSON = "json"
    XML = "xml"
    INI = "ini"
    RC = "rc"
    RESW = "resw"
    RESJSON = "resjson"
    QTTS = "qtts"
    JOOMLA = "joomla"
    CHROME = "chrome"
    DTD = "dtd"
    DKLANG = "dklang"
    FLEX = "flex"
    NSH = "nsh"
    WXL = "wxl"
    XLIFF = "xliff"
    HTML = "html"
    HAML = "haml"
    TXT = "txt"
    CSV = "csv"
    MD = "md"
    FLSNP = "flsnp"
    FM_HTML = "fm_html"
    FM_MD = "fm_md"
    MEDIAWIKI = "mediawiki"
    DOCX = "docx"
    SBV = "sbv"
    VTT = "vtt"
    SRT = "srt"
    XLIFF_TWO = "xliff_two"
    MDX_V1 = "mdx_v1"
    MDX_V2 = "mdx_v2"
    VSDX = "vsdx"
    XLSX = "xlsx"
    PROPERTIES_PLAY = "properties_play"
    PROPERTIES_XML = "properties_xml"
    MAXTHON = "maxthon"
    GO_JSON = "go_json"
    DITA = "dita"
    IDML = "idml"
    MIF = "mif"
    STRINGSDICT = "stringsdict"
    PLIST = "plist"
    VDF = "vdf"
    STF = "stf"
    TOML = "toml"
    CONTENTFUL_RT = "contentful_rt"
    SVG = "svg"
    JS = "js"
    COFFEE = "coffee"
    TS = "ts"
    I18NEXT_JSON = "i18next_json"
    XAML = "xaml"
    ARB = "arb"
    ADOC = "adoc"
    FBT = "fbt"
    WEBXML = "webxml"
    NESTJS_I18N = "nestjs_i18n"
    LOC = "loc"


class EscapeQuotes(Enum):
    """
    Values available:
        0 - Do not escape single quote
        1 - Escape single quote by another single quote
        2 - Escape single quote by a backslash
        3 - Escape single quote by another single quote only in strings containing variables
    """
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


class ExportQuotes(Enum):
    SINGLE = "single"
    DOUBLE = "double"


class FileUpdateOption(Enum):
    CLEAR_TRANSLATIONS_AND_APPROVALS = "clear_translations_and_approvals"
    KEEP_TRANSLATIONS = "keep_translations"
    KEEP_TRANSLATIONS_AND_APPROVALS = "keep_translations_and_approvals"


class FilePatchPath(Enum):
    BRANCH_ID = "/branchId"
    DIRECTORY_ID = "/directoryId"
    NAME = "/name"
    TITLE = "/title"
    CONTEXT = "/context"
    PRIORITY = "/priority"
    IMPORT_OPTIONS_CLEAN_TAGS_AGGRESSIVELY = "/importOptions/cleanTagsAggressively"
    IMPORT_OPTIONS_TRANSLATE_HIDDEN_TEXT = "/importOptions/translateHiddenText"
    IMPORT_OPTIONS_TRANSLATE_HYPERLINK_URLS = "/importOptions/translateHyperlinkUrls"
    IMPORT_OPTIONS_TRANSLATE_HIDDEN_ROWS_AND_COLUMNS = (
        "/importOptions/translateHiddenRowsAndColumns"
    )
    IMPORT_OPTIONS_IMPORT_NOTES = "/importOptions/importNotes"
    IMPORT_OPTIONS_IMPORT_HIDDEN_SLIDES = "/importOptions/importHiddenSlides"
    IMPORT_OPTIONS_FIRST_LINE_CONTAINS_HEADER = "/importOptions/firstLineContainsHeader"
    IMPORT_OPTIONS_IMPORT_TRANSLATIONS = "/importOptions/importTranslations"
    IMPORT_OPTIONS_SCHEME = "/importOptions/scheme"
    IMPORT_OPTIONS_TRANSLATE_CONTENT = "/importOptions/translateContent"
    IMPORT_OPTIONS_TRANSLATE_ATTRIBUTES = "/importOptions/translateAttributes"
    IMPORT_OPTIONS_CONTENT_SEGMENTATION = "/importOptions/contentSegmentation"
    IMPORT_OPTIONS_TRANSLATABLE_ELEMENTS = "/importOptions/translatableElements"
    IMPORT_OPTIONS_SRX_STORAGE_ID = "/importOptions/srxStorageId"
    IMPORT_OPTIONS_CUSTOM_SEGMENTATION = "/importOptions/customSegmentation"
    EXPORT_OPTIONS_EXPORT_PATTERN = "/exportOptions/exportPattern"
    EXPORT_OPTIONS_ESCAPE_QUOTES = "/exportOptions/escapeQuotes"
    EXCLUDED_TARGET_LANGUAGES = "/excludedTargetLanguages"
    ATTACH_LABEL_IDS = "/attachLabelIds"
    DETACH_LABEL_IDS = "/detachLabelIds"
    IMPORT_OPTIONS_IMPORT_KEY_AS_SOURCE = "/importOptions/importKeyAsSource"
    IMPORT_OPTIONS_IMPORT_HIDDEN_SHEETS = "/importOptions/importHiddenSheets"
    IMPORT_OPTIONS_HIDE_ATTRIBUTE_VALUES = "/importOptions/hideAttributeValues"
    IMPORT_OPTIONS_EXCLUDED_ELEMENTS = "/importOptions/excludedElements"
    IMPORT_OPTIONS_EXCLUDE_INCLUDE_DIRECTIVES = "/importOptions/excludeIncludeDirectives"
    IMPORT_OPTIONS_EXCLUDED_FRONT_MATTER_ELEMENTS = "/importOptions/excludedFrontMatterElements"
    IMPORT_OPTIONS_EXCLUDE_CODE_BLOCKS = "/importOptions/excludeCodeBlocks"
    IMPORT_OPTIONS_INLINE_TAGS = "/importOptions/inlineTags"
    IMPORT_OPTIONS_INLINE_HYPERLINK_TEXT = "/importOptions/inlineHyperlinkText"
    IMPORT_OPTIONS_TRANSLATE_DOC_PROPERTIES = "/importOptions/translateDocProperties"
    IMPORT_OPTIONS_TRANSLATE_COMMENTS = "/importOptions/translateComments"
    IMPORT_OPTIONS_IGNORE_WHITESPACE_STYLES = "/importOptions/ignoreWhitespaceStyles"
    IMPORT_OPTIONS_ADD_TAB_AS_CHARACTER = "/importOptions/addTabAsCharacter"
    IMPORT_OPTIONS_ADD_LINE_SEPARATOR_AS_CHARACTER = "/importOptions/addLineSeparatorAsCharacter"
    IMPORT_OPTIONS_LINE_SEPARATOR_REPLACEMENT = "/importOptions/lineSeparatorReplacement"
    IMPORT_OPTIONS_REPLACE_NO_BREAK_HYPHEN_TAG = "/importOptions/replaceNoBreakHyphenTag"
    IMPORT_OPTIONS_IGNORE_SOFT_HYPHEN_TAG = "/importOptions/ignoreSoftHyphenTag"
    IMPORT_OPTIONS_COMPLEX_FIELD_DEFINITIONS_TO_EXTRACT = (
        "/importOptions/complexFieldDefinitionsToExtract"
    )
    IMPORT_OPTIONS_TRANSLATE_WORD_HEADERS_FOOTERS = "/importOptions/translateWordHeadersFooters"
    IMPORT_OPTIONS_TRANSLATE_WORD_GRAPHIC_NAME = "/importOptions/translateWordGraphicName"
    IMPORT_OPTIONS_TRANSLATE_WORD_GRAPHIC_DESCRIPTION = (
        "/importOptions/translateWordGraphicDescription"
    )
    IMPORT_OPTIONS_IGNORE_WORD_FONT_COLORS = "/importOptions/ignoreWordFontColors"
    IMPORT_OPTIONS_WORD_FONT_COLORS_MIN_IGNORANCE_THRESHOLD = (
        "/importOptions/wordFontColorsMinIgnoranceThreshold"
    )
    IMPORT_OPTIONS_WORD_FONT_COLORS_MAX_IGNORANCE_THRESHOLD = (
        "/importOptions/wordFontColorsMaxIgnoranceThreshold"
    )
    IMPORT_OPTIONS_EXCLUDE_WORD_STYLES = "/importOptions/excludeWordStyles"
    IMPORT_OPTIONS_TRANSLATE_WORD_IN_EXCLUDE_STYLE_MODE = (
        "/importOptions/translateWordInExcludeStyleMode"
    )
    IMPORT_OPTIONS_WORD_HIGHLIGHT_COLORS = "/importOptions/wordHighlightColors"
    IMPORT_OPTIONS_TRANSLATE_WORD_IN_EXCLUDE_HIGHLIGHT_MODE = (
        "/importOptions/translateWordInExcludeHighlightMode"
    )
    IMPORT_OPTIONS_TRANSLATE_WORD_EXCLUDE_COLORS = "/importOptions/translateWordExcludeColors"
    IMPORT_OPTIONS_WORD_EXCLUDED_COLORS = "/importOptions/wordExcludedColors"
    IMPORT_OPTIONS_TRANSLATE_EXCEL_CELLS_COPIED = "/importOptions/translateExcelCellsCopied"
    IMPORT_OPTIONS_TRANSLATE_EXCEL_SHEET_NAMES = "/importOptions/translateExcelSheetNames"
    IMPORT_OPTIONS_EXCEL_EXCLUDED_COLORS = "/importOptions/excelExcludedColors"
    IMPORT_OPTIONS_TRANSLATE_EXCEL_DIAGRAM_DATA = "/importOptions/translateExcelDiagramData"
    IMPORT_OPTIONS_TRANSLATE_EXCEL_DRAWINGS = "/importOptions/translateExcelDrawings"
    EXPORT_OPTIONS_EXPORT_QUOTES = "/exportOptions/exportQuotes"
    EXPORT_OPTIONS_ESCAPE_SPECIAL_CHARACTERS = "/exportOptions/escapeSpecialCharacters"
    EXPORT_OPTIONS_ALLOW_WORD_STYLE_OPTIMIZATION = "/exportOptions/allowWordStyleOptimization"
    EXPORT_OPTIONS_TRANSLATE_EXCEL_EXCLUDE_COLORS = "/exportOptions/translateExcelExcludeColors"
    FIELDS = "/fields"  # Enterprise only
    FIELD = "/fields/{fieldSlug}"  # Enterprise only


class ListProjectBranchesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TITLE = "title"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    EXPORT_PATTERN = "exportPattern"
    PRIORITY = "priority"


class ListDirectoriesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TITLE = "title"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    EXPORT_PATTERN = "exportPattern"
    PRIORITY = "priority"


class ListFilesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TITLE = "title"
    STATUS = "status"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    EXPORT_PATTERN = "exportPattern"
    PRIORITY = "priority"


class EscapeSpecialCharacters(Enum):
    """
    Values available:
        0 - Do not escape special characters
        1 - Escape special characters by a backslash
    """
    ZERO = 0
    ONE = 1


class MarkdownMarker(Enum):
    ASTERISK = "asterisk"
    UNDERSCORE = "underscore"


class UnorderedListBullet(Enum):
    ASTERISKS = "asterisks"
    PLUS = "plus"
    DASH = "dash"


class TableColumnWidth(Enum):
    CONSOLIDATE = "consolidate"
    EVENLY_DISTRIBUTE_CELLS = "evenly_distribute_cells"


class FrontMatterQuotes(Enum):
    AUTO = "auto"
    SINGLE = "single"
    DOUBLE = "double"
