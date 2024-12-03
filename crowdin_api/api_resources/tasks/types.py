from typing import Any, Iterable, Union, Optional

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.tasks.enums import (
    TaskOperationPatchPath,
    VendorTaskOperationPatchPath,
    ConfigTaskOperationPatchPath,
)
from crowdin_api.typing import TypedDict


class CrowdinTaskAssignee(TypedDict, total=False):
    id: int
    wordsCount: int


class TaskPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TaskOperationPatchPath


class VendorPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: VendorTaskOperationPatchPath


class ConfigPatchRequest(TypedDict):
    value: Union[str, int]
    op: PatchOperation
    path: ConfigTaskOperationPatchPath


class TaskSettingsTemplateConfigLanguage(TypedDict):
    languageId: str
    userIds: Optional[Iterable[int]]


class TaskSettingsTemplateLanguages(TypedDict):
    languages: Iterable[TaskSettingsTemplateConfigLanguage]


class EnterpriseTaskAssignedTeams(TypedDict, total=False):
    id: int
    wordsCount: int


class EnterpriseTaskSettingsTemplateConfigLanguage(TypedDict):
    languageId: str
    userIds: Optional[Iterable[int]]
    teamIds: Optional[Iterable[int]]


class EnterpriseTaskSettingsTemplateLanguages(TypedDict):
    languages: Iterable[EnterpriseTaskSettingsTemplateConfigLanguage]
