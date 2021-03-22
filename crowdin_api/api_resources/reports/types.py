from typing import Iterable, Union

from crowdin_api.api_resources.reports.enums import FuzzyRateMode, SimpleRateMode
from crowdin_api.typing import TypedDict


class SimpleRegularRate(TypedDict):
    mode: SimpleRateMode
    value: Union[float, int]


class SimpleIndividualRate(TypedDict):
    languageIds: Iterable[str]
    rates: Iterable[SimpleRegularRate]


class FuzzyRegularRate(TypedDict):
    mode: FuzzyRateMode
    value: Union[float, int]


class FuzzyIndividualRate(TypedDict):
    languageIds: Iterable[str]
    rates: Iterable[FuzzyRegularRate]
