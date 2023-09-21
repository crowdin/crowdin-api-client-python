from typing import Iterable, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.reports.enums import (
    FuzzyRateMode,
    SimpleRateMode,
    ReportSettingsTemplatesPatchPath,
    MatchType
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
