from enum import Enum


class HasManagerAccess(Enum):
    TRUE = 1
    FALSE = 0


class ProjectType(Enum):
    FILE_BASED = 0
    STRING_BASED = 1


class ProjectVisibility(Enum):
    PRIVATE = "private"
    OPEN = "open"


class ProjectLanguageAccessPolicy(Enum):
    OPEN = "open"
    MODERATE = "moderate"


class ProjectPatchPath(Enum):
    NAME = "/name"
    TARGET_LANGUAGE_IDS = "/targetLanguageIds"
    CNAME = "/cname"
    VISIBILITY = "/visibility"
    LANGUAGE_ACCESS_POLICY = "/languageAccessPolicy"
    DESCRIPTION = "/description"
    TRANSLATE_DUPLICATES = "/translateDuplicates"
    IS_MT_ALLOWED = "/isMtAllowed"
    AUTO_SUBSTITUTION = "/autoSubstitution"
    SKIP_UNTRANSLATED_STRINGS = "/skipUntranslatedStrings"
    SKIP_UNTRANSLATED_FILES = "/skipUntranslatedFiles"
    EXPORT_APPROVED_ONLY = "/exportApprovedOnly"
    AUTO_TRANSLATE_DIALECTS = "/autoTranslateDialects"
    PUBLIC_DOWNLOADS = "/publicDownloads"
    USE_GLOBAL_TM = "/useGlobalTm"
    NORMALIZE_PLACEHOLDER = "normalizePlaceholder"
    SAVE_META_INFO_IN_SOURCE = "saveMetaInfoInSource"
    IN_CONTEXT = "/inContext"
    IN_CONTEXT_PSEUDO_LANGUAGE_ID = "/inContextPseudoLanguageId"
    QA_CHECK_IS_ACTIVE = "/qaCheckIsActive"
    QA_CHECK_CATEGORIES = "/qaCheckCategories"
    QA_CHECK_CATEGORY = "/qaCheckCategories/{category}"
    QA_CHECKS_IGNORABLE_CATEGORIES = "/qaChecksIgnorableCategories"
    QA_CHECKS_IGNORABLE_CATEGORY = "/qaChecksIgnorableCategories/{category}"
    LANGUAGE_MAPPING = "/languageMapping"
    LANGUAGE_MAPPING_ID = "/languageMapping/{languageId}"
    LANGUAGE_MAPPING_KEY = "/languageMapping/{languageId}/{mappingKey}"


class ProjectTranslateDuplicates(Enum):
    SHOW = 0
    HIDE_REGULAR_DETECTION = 1
    SHOW_AUTO_TRANSLATE = 2
    SHOW_REGULAR_DETECTION = 3
    HIDE_STRICT_DETECTION = 4
    SHOW_STRICT_DETECTION = 5


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


class EscapeSpecialCharacters(Enum):
    """
    Defines whether any special characters (=, :, ! and #) should be escaped by backslash in
    exported translations.
    You can add escape_special_characters per-file option. *

    Acceptable values are:
        0 - Do not escape special characters
        1 - Escape special characters by a backslash
    """
    ZERO = 0
    ONE = 1


class ProjectFilePatchPath(Enum):
    FORMAT = "/format"
    SETTINGS = "/settings"
