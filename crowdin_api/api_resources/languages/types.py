from typing import List, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.languages.enums import LanguagesPatchPath
from crowdin_api.typing import TypedDict


class LanguagesPatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: PatchOperation
    path: LanguagesPatchPath
