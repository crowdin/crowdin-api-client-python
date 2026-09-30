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


class HourlyBaseRates(TypedDict):
    hourly: float


class HourlyIndividualRate(TypedDict):
    languageIds: Iterable[str]
    userIds: Iterable[int]
    hourly: float


class PostEditingIndividualRate(TypedDict):
    languageIds: Iterable[str]
    userIds: Iterable[int]
    fullTranslation: float
    proofread: float


class PostEditingNetRateSchemes(TypedDict, total=False):
    tmMatch: Iterable[Match]
    mtMatch: Iterable[Match]
    aiMatch: Iterable[Match]
    suggestionMatch: Iterable[Match]


class PostEditingConfig(TypedDict, total=False):
    """
    Report settings template config for post-editing templates.
    """

    baseRates: BaseRates
    individualRates: Iterable[PostEditingIndividualRate]
    netRateSchemes: PostEditingNetRateSchemes
    calculateInternalMatches: bool
    includePreTranslatedStrings: bool
    useCategoryBasedProofreadRates: bool
    useTmEditDistance: bool


class HourlyConfig(TypedDict):
    """
    Report settings template config for hourly templates (unit `hours`).
    """

    baseRates: HourlyBaseRates
    individualRates: Iterable[HourlyIndividualRate]
