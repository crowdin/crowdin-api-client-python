from enum import Enum


class ExportFormat(Enum):
    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"


class ScopeType(Enum):
    ORGANIZATION = "organization"
    GRPOUP = "group"
    PROJECT = "project"


class ReportName(Enum):
    PRE_TRANSLATE_ACCURACY = "pre-translate-accuracy"
    COSTS_ESTIMATION = "costs-estimation"
    TRANSLATION_COSTS = "translation-costs"
    TOP_MEMBERS = "top-members"
    CONTRIBUTION_RAW_DATA = "contribution-raw-data"
    COSTS_ESTIMATION_POST_EDITING = "costs-estimation-pe"
    TRANSLATION_COSTS_POST_EDITING = "translation-costs-pe"


class Unit(Enum):
    STRINGS = "strings"
    WORDS = "words"
    CHARS = "chars"
    CHARS_WITH_SPACES = "chars_with_spaces"


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"
    GBP = "GBP"
    AUD = "AUD"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    SEK = "SEK"
    NZD = "NZD"
    MXN = "MXN"
    SGD = "SGD"
    HKD = "HKD"
    NOK = "NOK"
    KRW = "KRW"
    TRY = "TRY"
    RUB = "RUB"
    INR = "INR"
    BRL = "BRL"
    ZAR = "ZAR"
    GEL = "GEL"
    UAH = "UAH"


class SchemaMode(Enum):
    SIMPLE = "simple"
    FUZZY = "fuzzy"


class Format(Enum):
    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"


class SimpleRateMode(Enum):
    NO_MATCH = "no_match"
    TM_MATCH = "tm_match"
    APPROVAL = "approval"


class FuzzyRateMode(Enum):
    NO_MATCH = "no_match"
    PERFECT = "perfect"
    ONE_HUNDRED = "100"
    MORE_NINETY_FIVE = "99-95"
    MORE_NINETY = "94-90"
    MORE_EIGHTY = "89-80"
    APPROVAL = "approval"


class GroupBy(Enum):
    USER = "user"
    LANGUAGE = "language"


class ContributionMode:
    TRANSLATIONS = "translations"
    APPROVALS = "approvals"
    VOTES = "votes"


class ReportSettingsTemplatesPatchPath(Enum):
    NAME = "name"
    CURRENCY = "currency"
    UNIT = "unit"
    MODE = "mode"
    CONFIG = "config"


class ReportLabelIncludeType(Enum):
    STRINGS_WITH_LABEL = "strings_with_label"
    STRINGS_WITHOUT_LABEL = "strings_without_label"


class MatchType(Enum):
    PERFECT = "perfect"
    OPTION_100 = "100"
    OPTION_99_82 = "99-82"
    OPTION_81_60 = "81-60"
