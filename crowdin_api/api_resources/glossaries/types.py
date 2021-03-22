from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.glossaries.enums import GlossaryPatchPath, TermPatchPath
from crowdin_api.typing import TypedDict


class GlossaryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: GlossaryPatchPath


class TermPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TermPatchPath
