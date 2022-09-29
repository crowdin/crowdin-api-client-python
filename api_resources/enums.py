from enum import Enum


class PatchOperation(Enum):
    TEST = "test"
    REPLACE = "replace"
    REMOVE = "remove"


class ExportFormat(Enum):
    TBX = "tbx"
    CSV = "csv"
    XLSX = "xlsx"


class DenormalizePlaceholders(Enum):
    ENABLE = 1
    DISABLE = 0


class PluralCategoryName(Enum):
    ZERO = "zero"
    ONE = "one"
    TWO = "two"
    FEW = "few"
    MANY = "many"
    OTHER = "other"


class ExportProjectTranslationFormat(Enum):
    XLIFF = "xliff"
    ANDROID = "android"
    MACOSX = "macosx"
