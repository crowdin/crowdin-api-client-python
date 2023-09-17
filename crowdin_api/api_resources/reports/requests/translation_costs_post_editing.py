from abc import ABC
from datetime import datetime
from typing import Iterable, Optional

from crowdin_api.api_resources.reports.enums import (
    Unit,
    Currency,
    Format,
    GroupBy
)
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
    mtMatch: Iterable[Match]
    suggestionMatch: Iterable[Match]


class SchemaBase(ABC):
    unit: Optional[Unit]
    currency: Optional[Currency]
    format: Optional[Format]
    baseRates: BaseRates
    individualRates: Iterable[IndividualRate]
    netRateSchemes: NetRateSchemes


class GeneralSchema(SchemaBase):
    groupBy: Optional[GroupBy]
    dateFrom: Optional[datetime]
    dateTo: Optional[datetime]
    languageId: Optional[str]
    userIds: Optional[Iterable[int]]
    fileIds: Optional[Iterable[int]]
    directoryIds: Optional[Iterable[int]]
    branchIds: Optional[Iterable[int]]


class ByTaskSchema(SchemaBase):
    taskId: Optional[int]


class TranslationCostsPostEditingGenerateReportRequest:
    name = "translation-costs-pe"
    schema: SchemaBase
