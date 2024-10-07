from typing import Iterable

from crowdin_api.typing import TypedDict

from crowdin_api.api_resources.translations.enums import PreTranslationEditOperation


class FallbackLanguages(TypedDict):
    languageId: Iterable[str]


class EditPreTranslationScheme(TypedDict):
    op: PreTranslationEditOperation
    path: str
    value: str
