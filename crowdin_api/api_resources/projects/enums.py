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
    LANGUAGE_MAPPING = "/languageMapping"
    LANGUAGE_MAPPING_ID = "/languageMapping/{languageId}"
    LANGUAGE_MAPPING_KEY = "/languageMapping/{languageId}/{mappingKey}"
