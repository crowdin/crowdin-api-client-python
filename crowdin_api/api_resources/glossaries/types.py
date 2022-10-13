from typing import Any, Optional, Iterable

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.glossaries.enums import (
    GlossaryPatchPath,
    TermPatchPath,
    GlossaryFormat,
    GlossaryExportFields,
)
from crowdin_api.typing import TypedDict


class GlossaryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: GlossaryPatchPath


class GlossarySchemaRequest(TypedDict):
    format: Optional[GlossaryFormat]
    exportFields: Optional[Iterable[GlossaryExportFields]]


class TermPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TermPatchPath


class LanguagesDetails(TypedDict):
    languageId: str
    definition: str
    note: Optional[str]
