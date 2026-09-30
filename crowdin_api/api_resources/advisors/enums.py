from enum import Enum


class AdvisorInspectorMode(Enum):
    AUTO = "auto"
    ALL = "all"


class AdvisorInsightStatus(Enum):
    PENDING = "pending"
    CHECKING = "checking"
    OUTDATED = "outdated"
    DONE = "done"


class AdvisorInsightOutcome(Enum):
    FLAGGED = "flagged"
    CLEAR = "clear"
    NOT_APPLICABLE = "not_applicable"


class AdvisorInsightPatchPath(Enum):
    IS_DISMISSED = "/isDismissed"


class AdvisorInsightMetricUnit(Enum):
    PERCENT = "percent"
    COUNT = "count"


class AdvisorInsightMetricTone(Enum):
    DEFAULT = "default"
    SUCCESS = "success"
    DANGER = "danger"


class AdvisorInsightMetricSource(Enum):
    DETERMINISTIC = "deterministic"
    AI = "ai"
    APP = "app"
