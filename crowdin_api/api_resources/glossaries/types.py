from typing import Any, Iterable, Optional, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.glossaries.enums import (
    GlossaryExportFields,
    GlossaryExportGender,
    GlossaryExportPartOfSpeech,
    GlossaryExportStatus,
    GlossaryExportTermType,
    GlossaryExportType,
    GlossaryFormat,
    GlossaryPatchPath,
    TermPatchPath,
)
from crowdin_api.typing import TypedDict


class GlossaryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: GlossaryPatchPath


class GlossarySchemaRequest(TypedDict):
    format: Optional[GlossaryFormat]
    # Enterprise also accepts custom field slugs: `field_{fieldSlug}` / `conceptField_{fieldSlug}`
    exportFields: Optional[Iterable[Union[GlossaryExportFields, str]]]
    exportType: Optional[GlossaryExportType]
    statuses: Optional[Iterable[GlossaryExportStatus]]
    partsOfSpeech: Optional[Iterable[GlossaryExportPartOfSpeech]]
    types: Optional[Iterable[GlossaryExportTermType]]
    genders: Optional[Iterable[GlossaryExportGender]]
    authorIds: Optional[Iterable[int]]
    languageIds: Optional[Iterable[str]]
    text: Optional[str]
    # caseSensitive, searchStrict and searchFullMatch must be used together with `text`
    caseSensitive: Optional[bool]
    searchStrict: Optional[bool]
    searchFullMatch: Optional[bool]
    # UTC, ISO 8601, e.g. "2024-01-23T07:00:14+00:00"
    dateFrom: Optional[str]
    dateTo: Optional[str]
    # Deprecated in favor of the plural filters above; the API rejects requests combining a
    # singular filter with its plural counterpart.
    status: Optional[GlossaryExportStatus]
    partOfSpeech: Optional[GlossaryExportPartOfSpeech]
    type: Optional[GlossaryExportTermType]
    gender: Optional[GlossaryExportGender]
    authorId: Optional[int]


class OrganizationConcordanceSearchRequest(TypedDict):
    sourceLanguageId: str
    targetLanguageId: str
    expressions: Iterable[str]
    userId: Optional[int]  # Crowdin only


class TermPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TermPatchPath


class LanguagesDetails(TypedDict):
    languageId: str
    definition: str
    note: Optional[str]
