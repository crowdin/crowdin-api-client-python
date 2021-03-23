from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.translation_memory.enums import TranslationMemoryPatchPath
from crowdin_api.typing import TypedDict


class TranslationMemoryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TranslationMemoryPatchPath
