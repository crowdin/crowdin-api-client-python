from enum import Enum


class ExportFormat(Enum):
    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"


class ScopeType(Enum):
    ORGANIZATION = "organization"
    GRPOUP = "group"
    GROUP = "group"
    PROJECT = "project"


class ReportName(Enum):
    PRE_TRANSLATE_ACCURACY = "pre-translate-accuracy"
    # Deprecated: no longer supported by the API
    COSTS_ESTIMATION = "costs-estimation"
    # Deprecated: no longer supported by the API
    TRANSLATION_COSTS = "translation-costs"
    TOP_MEMBERS = "top-members"
    CONTRIBUTION_RAW_DATA = "contribution-raw-data"
    COSTS_ESTIMATION_POST_EDITING = "costs-estimation-pe"
    TRANSLATION_COSTS_POST_EDITING = "translation-costs-pe"
    TRANSLATOR_ACCURACY = "translator-accuracy"
    SOURCE_CONTENT_UPDATES = "source-content-updates"
    PROJECT_MEMBERS = "project-members"
    EDITOR_ISSUES = "editor-issues"
    QA_CHECK_ISSUES = "qa-check-issues"
    SAVING_ACTIVITY = "saving-activity"
    TRANSLATION_ACTIVITY = "translation-activity"
    TIME_SPENT = "time-spent"
    # Enterprise only
    TASK_USAGE = "task-usage"


class GroupReportName(Enum):
    """
    Report names for Enterprise group and organization reports.
    """

    GROUP_TRANSLATION_COSTS_POST_EDITING = "group-translation-costs-pe"
    GROUP_TOP_MEMBERS = "group-top-members"
    GROUP_TASK_USAGE = "group-task-usage"
    GROUP_QA_CHECK_ISSUES = "group-qa-check-issues"
    GROUP_TRANSLATION_ACTIVITY = "group-translation-activity"
    GROUP_SOURCE_CONTENT_UPDATES = "group-source-content-updates"
    GROUP_TIME_SPENT = "group-time-spent"
    GROUP_PRE_TRANSLATE_ACCURACY = "group-pre-translate-accuracy"
    GROUP_TRANSLATOR_ACCURACY = "group-translator-accuracy"
    GROUP_SAVING_ACTIVITY = "group-saving-activity"


class Unit(Enum):
    STRINGS = "strings"
    WORDS = "words"
    CHARS = "chars"
    CHARS_WITH_SPACES = "chars_with_spaces"
    # Only for hourly report settings templates
    HOURS = "hours"


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
    DDK = "DDK"
    PLN = "PLN"


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
    # Only for time spent reports
    TASK = "task"
    # Only for task usage reports
    TYPE = "type"
    # Only for group and organization reports
    PROJECT = "project"


class ContributionMode:
    TRANSLATIONS = "translations"
    APPROVALS = "approvals"
    VOTES = "votes"


class ReportSettingsTemplatesPatchPath(Enum):
    NAME = "/name"
    CURRENCY = "/currency"
    UNIT = "/unit"
    # Crowdin project report settings templates only
    MODE = "/mode"
    CONFIG = "/config"
    # Enterprise organization report settings templates only
    IS_PUBLIC = "/isPublic"


class ReportLabelIncludeType(Enum):
    STRINGS_WITH_LABEL = "strings_with_label"
    STRINGS_WITHOUT_LABEL = "strings_without_label"


class MatchType(Enum):
    PERFECT = "perfect"
    OPTION_100 = "100"
    OPTION_99_82 = "99-82"
    OPTION_81_60 = "81-60"


class SavingActivityMode(Enum):
    CURRENCY = "currency"
    RELATIVE = "relative"


class EditorIssueType(Enum):
    GENERAL_QUESTION = "general_question"
    TRANSLATION_MISTAKE = "translation_mistake"
    CONTEXT_REQUEST = "context_request"
    SOURCE_MISTAKE = "source_mistake"


class TaskType(Enum):
    """
    Task type for `typeTasks` report schema field.

    0 - translate, 1 - proofread, 2 - translate by vendor, 3 - proofread by vendor.
    """

    TRANSLATE = 0
    PROOFREAD = 1
    TRANSLATE_BY_VENDOR = 2
    PROOFREAD_BY_VENDOR = 3


class TaskUsageReportType(Enum):
    WORKLOAD = "workload"
    CREATED_VS_RESOLVED = "created-vs-resolved"
    PERFORMANCE = "performance"
    TIME = "time"
    COST = "cost"


class TaskUsageStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CLOSED = "closed"
    REVIEW = "review"
