from typing import Optional

from crowdin_api.api_resources.enums import PluralCategoryName
from crowdin_api.typing import TypedDict


class _ValidateQaChecksRequestRequired(TypedDict):
    stringId: int
    languageId: str
    text: str


class ValidateQaChecksRequest(_ValidateQaChecksRequestRequired, total=False):
    pluralCategoryName: Optional[PluralCategoryName]
