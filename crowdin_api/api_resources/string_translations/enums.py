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
