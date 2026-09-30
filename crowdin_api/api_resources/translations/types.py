from typing import Dict, Iterable, Optional, Union
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.translations.enums import (
    PreTranslationEditOperation,
    PreTranslationPatchPath,
)


class FallbackLanguages(TypedDict):
    languageId: Iterable[str]


class EditPreTranslationScheme(TypedDict):
    op: PreTranslationEditOperation
    path: Union[PreTranslationPatchPath, str]
    value: str


class UploadTranslationRequest(TypedDict):
    storageId: int
    fileId: int
    importEqSuggestions: Optional[bool]
    autoApproveImported: Optional[bool]
    translateHidden: Optional[bool]
    addToTm: Optional[bool]


class ImportTranslationsOptions(TypedDict, total=False):
    """
    Import options for spreadsheet files in string-based projects.

    `scheme` maps column names (`none`, `identifier`, `sourceOrTranslation`, `translation`
    or a language identifier such as `en`) to column numbers, starting at 0.
    """

    scheme: Dict[str, int]
