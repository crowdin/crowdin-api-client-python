from abc import ABC
from datetime import datetime
from typing import Iterable, Union, Optional

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.reports.enums import (
    FuzzyRateMode,
    SimpleRateMode,
    ReportSettingsTemplatesPatchPath,
    MatchType,
    ReportLabelIncludeType
)
from crowdin_api.typing import TypedDict


class SimpleRegularRate(TypedDict):
    mode: SimpleRateMode
    value: Union[float, int]


class SimpleIndividualRate(TypedDict):
    languageIds: Iterable[str]
    rates: Iterable[SimpleRegularRate]


class SimpleSettingsTemplateRate(SimpleIndividualRate):
    userIds: Iterable[int]


class FuzzyRegularRate(TypedDict):
    mode: FuzzyRateMode
    value: Union[float, int]


class FuzzyIndividualRate(TypedDict):
    languageIds: Iterable[str]
    rates: Iterable[FuzzyRegularRate]


class TranslateStep(TypedDict):
    regularRates: Iterable[FuzzyRegularRate]
    individualRates: Iterable[FuzzyIndividualRate]


class StepTypes(TypedDict):
    stepTypes: Iterable[TranslateStep]


class Config(TypedDict):
    regularRates: Iterable[SimpleRegularRate]
    individualRates: Iterable[SimpleSettingsTemplateRate]


class ReportSettingsTemplatesPatchRequest(TypedDict):
    value: Union[str, int]
    op: PatchOperation
    path: ReportSettingsTemplatesPatchPath


class Match(TypedDict):
    matchType: MatchType
    price: float


class BaseRates(TypedDict):
    fullTranslation: float
    proofread: float


# class GenerateReportRequest(ABC):
#     pass
#
#
# class GenerateGroupReportRequest(ABC):
#     pass

# class CostEstimationPostEditingGenerateReportRequest:
#     class IndividualRate(TypedDict):
#         languageIds: Iterable[str]
#         userIds: Iterable[str]
#         fullTranslation: float
#         proofread: float
#
#     class NetRatesSchemes(TypedDict):
#         tmMatch: Iterable[Match]
#
#     class SchemaBase(ABC):
#         pass
#
#     class GeneralSchema(SchemaBase):
#         baseRates: BaseRates
#         individualRates: Iterable[IndividualRate]
#         netRateSchemes: NetRatesSchemes
#         languageId: Optional[str]
#         fileIds: Optional[Iterable[int]]
#         directoryIds: Optional[Iterable[int]]
#         branchIds: Optional[Iterable[int]]
#         dateFrom: Optional[datetime]
#         dateTo: Optional[datetime]
#         labelIds: Optional[Iterable[int]]
#         labelIncludeType: Optional[ReportLabelIncludeType]
#
#     class ByTaskSchema(SchemaBase):
#         baseRates: Optional[BaseRates]
#         individualRates: Optional[Iterable[IndividualRate]]
#         netRateSchemes: Optional[NetRatesSchemes]
#         taskId: Optional[int]
#
#     name = "costs-estimation-pe"
#     schema: SchemaBase
