from typing import Iterable, Optional
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.translations.enums import PreTranslationEditOperation


class FallbackLanguages(TypedDict):
    languageId: Iterable[str]


class EditPreTranslationScheme(TypedDict):
    op: PreTranslationEditOperation
    path: str
    value: str


class UploadTranslationRequest(TypedDict):
    storageId: int
    fileId: int
    importEqSuggestions: Optional[bool]
    autoApproveImported: Optional[bool]
    translateHidden: Optional[bool]
    addToTm: Optional[bool]
