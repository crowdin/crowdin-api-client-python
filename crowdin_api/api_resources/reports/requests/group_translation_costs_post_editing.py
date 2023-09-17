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
    # GenerateGroupReportRequest
)
from crowdin_api.typing import TypedDict


class IndividualRate:
    languageIds: Iterable[str]
    userIds: Iterable[int]
    fullTranslation: float
    proofread: float


class NetRateSchemes:
    tmMatch: Iterable[Match]
    mtMatch: Iterable[Match]
    suggestionMatch: Iterable[Match]


class SchemaBase(ABC):
    pass


class GeneralSchema(SchemaBase):
    projectIds: Optional[Iterable[int]]
    unit: Optional[Unit]
    currency: Optional[Currency]
    format: Optional[Format]
    baseRates: BaseRates
    individualRates: Iterable[IndividualRate]
    netRateSchemes: NetRateSchemes
    groupBy: Optional[GroupBy]
    dateFrom: Optional[datetime]
    dateTo: Optional[datetime]
    userIds: Optional[Iterable[int]]


class GroupTranslationCostsPostEditingGenerateGroupReportRequest:
    name = "group-translation-costs-pe"
    schema: SchemaBase
