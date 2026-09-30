from datetime import datetime
from typing import Any, Dict, Optional, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.advisors.enums import (
    AdvisorInspectorMode,
    AdvisorInsightMetricSource,
    AdvisorInsightMetricTone,
    AdvisorInsightMetricUnit,
    AdvisorInsightPatchPath,
)


class AdvisorInspectorOptions(TypedDict, total=False):
    mode: AdvisorInspectorMode
    promptId: int


class _AdvisorCheckInspectorRequired(TypedDict):
    key: str


class AdvisorCheckInspector(_AdvisorCheckInspectorRequired, total=False):
    options: Optional[AdvisorInspectorOptions]


class AdvisorInsightPatchRequest(TypedDict):
    op: PatchOperation
    path: AdvisorInsightPatchPath
    value: bool


class AdvisorInsightMetric(TypedDict, total=False):
    key: str
    value: Union[int, float]
    unit: AdvisorInsightMetricUnit
    threshold: Optional[Union[int, float]]
    tone: AdvisorInsightMetricTone
    source: AdvisorInsightMetricSource
    checkedAt: Optional[Union[datetime, str]]


class AdvisorInsightRecommendation(TypedDict, total=False):
    id: str
    primary: bool
    params: Dict[str, Any]
