from typing import Any

from crowdin_api.api_resources.custom_placeholders.enums import CustomPlaceholderPatchPath
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class CustomPlaceholderPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: CustomPlaceholderPatchPath
