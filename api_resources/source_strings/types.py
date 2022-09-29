from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_strings.enums import SourceStringsPatchPath
from crowdin_api.typing import TypedDict


class SourceStringsPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: SourceStringsPatchPath
