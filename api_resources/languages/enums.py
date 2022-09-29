from enum import Enum


class LanguageTextDirection(Enum):
    LEFT_TO_RIGHT = "ltr"
    RIGHT_TO_LEFT = "rtl"


class LanguagesPatchPath(Enum):
    NAME = "/name"
    TEXT_DIRECTION = "/textDirection"
    PLURAL_CATEGORY_NAMES = "/pluralCategoryNames"
    THREE_LETTERS_CODE = "/threeLettersCode"
    LOCALE_CODE = "/localeCode"
    DIALECT_OF = "/dialectOf"
