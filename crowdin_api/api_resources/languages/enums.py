from enum import Enum


class LanguageTextDirection(Enum):
    left_to_right = "ltr"
    right_to_left = "rtl"


class LanguagesPatchPath(Enum):
    name = "/name"
    textDirection = "/textDirection"
    pluralCategoryNames = "/pluralCategoryNames"
    threeLettersCode = "/threeLettersCode"
    localeCode = "/localeCode"
    dialectOf = "/dialectOf"
