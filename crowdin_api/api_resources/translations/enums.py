from enum import Enum


class PreTranslationApplyMethod(Enum):
    TM = "tm"
    MT = "mt"


class PreTranslationAutoApproveOption(Enum):
    ALL = "all"
    EXCEPT_AUTO_SUBSTITUTED = "exceptAutoSubstituted"
    PERFECT_MATCH_ONLY = "perfectMatchOnly"
    NONE = "none"


class CharTransformation(Enum):
    ASIAN = "asian"
    EUROPEAN = "european"
    ARABIC = "arabic"
    CYRILLIC = "cyrillic"
