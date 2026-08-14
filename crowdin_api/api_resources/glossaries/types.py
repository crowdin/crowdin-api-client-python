from typing import Any, Optional, Iterable

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.glossaries.enums import (
    GlossaryPatchPath,
    TermPatchPath,
    GlossaryFormat,
    GlossaryExportFields,
    GlossaryExportType,
    GlossaryExportStatus,
    GlossaryExportPartOfSpeech,
    GlossaryExportTermType,
    GlossaryExportGender,
)
from crowdin_api.typing import TypedDict


class GlossaryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: GlossaryPatchPath


class GlossarySchemaRequest(TypedDict):
    format: Optional[GlossaryFormat]
    exportFields: Optional[Iterable[GlossaryExportFields]]
    exportType: Optional[GlossaryExportType]
    statuses: Optional[Iterable[GlossaryExportStatus]]
    partsOfSpeech: Optional[Iterable[GlossaryExportPartOfSpeech]]
    types: Optional[Iterable[GlossaryExportTermType]]
    genders: Optional[Iterable[GlossaryExportGender]]
    authorIds: Optional[Iterable[int]]
    languageIds: Optional[Iterable[str]]
    # Deprecated in favor of the plural filters above; the API rejects requests combining a
    # singular filter with its plural counterpart.
    status: Optional[GlossaryExportStatus]
    partOfSpeech: Optional[GlossaryExportPartOfSpeech]
    type: Optional[GlossaryExportTermType]
    gender: Optional[GlossaryExportGender]
    authorId: Optional[int]


class TermPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TermPatchPath


class LanguagesDetails(TypedDict):
    languageId: str
    definition: str
    note: Optional[str]
