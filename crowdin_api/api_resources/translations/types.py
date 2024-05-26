from typing import Iterable

from crowdin_api.typing import TypedDict


class FallbackLanguages(TypedDict):
    languageId: Iterable[str]
