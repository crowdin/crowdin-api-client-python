from enum import Enum


class PreTranslationApplyMethod(Enum):
    TM = "tm"
    MT = "mt"
    AI = "ai"


class PreTranslationAutoApproveOption(Enum):
    ALL = "all"
    EXCEPT_AUTO_SUBSTITUTED = "exceptAutoSubstituted"
    PERFECT_MATCH_ONLY = "perfectMatchOnly"
    PERFECT_MATCH_APPROVED_ONLY = "perfectMatchApprovedOnly"
    NONE = "none"


class PreTranslationScope(Enum):
    UNTRANSLATED = "untranslated"
    TRANSLATED = "translated"
    ALL = "all"


class PreTranslationReplaceTranslationsOption(Enum):
    NONE = "none"
    AUTO_TRANSLATED = "autoTranslated"
    ALL = "all"


class CharTransformation(Enum):
    ASIAN = "asian"
    EUROPEAN = "european"
    ARABIC = "arabic"
    CYRILLIC = "cyrillic"


class PreTranslationEditOperation(Enum):
    REPLACE = "replace"
    TEST = "test"


class PreTranslationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class PreTranslationPatchPath(Enum):
    STATUS = "/status"
    PRIORITY = "/priority"
