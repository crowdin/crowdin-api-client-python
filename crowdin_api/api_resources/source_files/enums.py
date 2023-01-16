from enum import Enum


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class BranchPatchPath(Enum):
    NAME = "/name"
    TITLE = "/title"
    EXPORT_PATTERN = "/exportPattern"
    PRIORITY = "/priority"


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


class FileUpdateOption(Enum):
    CLEAR_TRANSLATIONS_AND_APPROVALS = "clear_translations_and_approvals"
    KEEP_TRANSLATIONS = "keep_translations"
    KEEP_TRANSLATIONS_AND_APPROVALS = "keep_translations_and_approvals"


class FilePatchPath(Enum):
    BRANCH_ID = "/branchId"
    DIRECTORY_ID = "/directoryId"
    NAME = "/name"
    TITLE = "/title"
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
