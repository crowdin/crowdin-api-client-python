from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.languages.enums import LanguagesPatchPath
from crowdin_api.typing import TypedDict


class LanguagesPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: LanguagesPatchPath
