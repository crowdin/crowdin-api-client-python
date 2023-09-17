from abc import ABC
from datetime import datetime
from typing import Iterable, Optional

from crowdin_api.api_resources.reports.enums import ReportLabelIncludeType
from crowdin_api.api_resources.reports.types import (
    Match,
    BaseRates,
    # GenerateReportRequest
)
from crowdin_api.typing import TypedDict


class IndividualRate(TypedDict):
    languageIds: Iterable[str]
    userIds: Iterable[int]
    fullTranslation: float
    proofread: float


class NetRateSchemes(TypedDict):
    tmMatch: Iterable[Match]


class SchemaBase(ABC):
    pass


class GeneralSchema(SchemaBase):
    baseRates: BaseRates
    individualRates: Iterable[IndividualRate]
    netRateSchemes: NetRateSchemes
    languageId: Optional[str]
    fileIds: Optional[Iterable[int]]
    directoryIds: Optional[Iterable[int]]
    branchIds: Optional[Iterable[int]]
    dateFrom: Optional[datetime]
    dateTo: Optional[datetime]
    labelIds: Optional[Iterable[int]]
    labelIncludeType: Optional[ReportLabelIncludeType]


class ByTaskSchema(SchemaBase):
    baseRates: Optional[BaseRates]
    individualRates: Optional[Iterable[IndividualRate]]
    netRateSchemes: Optional[NetRateSchemes]
    taskId: Optional[int]


class CostEstimationPostEditingGenerateReportRequest(TypedDict):
    name = "costs-estimation-pe"  # TODO: test
    schema: SchemaBase
