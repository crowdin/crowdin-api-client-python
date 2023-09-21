from typing import Iterable
from crowdin_api.api_resources.reports.types import Match
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
