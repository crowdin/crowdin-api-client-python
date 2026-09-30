from enum import Enum


class PreTranslationApplyMethod(Enum):
    TM = "tm"
    MT = "mt"


class VoteMark(Enum):
    UP = "up"
    DOWN = "down"


class ListTranslationApprovalsOrderBy(Enum):
    ID = "id"
    CREATED_AT = "createdAt"


class ListLanguageTranslationsOrderBy(Enum):
    TEXT = "text"
    STRING_ID = "stringId"
    TRANSLATION_ID = "translationId"
    CREATED_AT = "createdAt"


class ListStringTranslationsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    RATING = "rating"
    CREATED_AT = "createdAt"


class TranslationProvider(Enum):
    TM = "tm"
    GLOBAL_TM = "global_tm"
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    CROWDIN = "crowdin"
    DEEPL = "deepl"
    AMAZON = "amazon"
    GOOGLE_AUTOML = "google_automl"
    MODERNMT = "modernmt"
    CUSTOM_MT = "custom_mt"
    AI = "ai"
