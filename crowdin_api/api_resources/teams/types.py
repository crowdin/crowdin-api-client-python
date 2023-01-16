from typing import Iterable, Union, Optional, Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.teams.enums import TeamPatchPath, TeamRole
from crowdin_api.typing import TypedDict


class TeamPatchRequest(TypedDict):
    value: Union[str, bool, Iterable[int], Iterable[dict]]
    op: PatchOperation
    path: TeamPatchPath


class WorkflowStepId(TypedDict):
    workflowStepIds: Union[str, Iterable[int]]


class Permissions(TypedDict):
    it: WorkflowStepId
    de: WorkflowStepId


class LanguageData(TypedDict):
    allContent: bool
    workflowStepIds: Optional[Iterable[Any]]


class LanguagesAccessData(TypedDict):
    it: LanguageData
    uk: LanguageData


class RolePermission(TypedDict):
    allLanguages: bool
    languagesAccess: Optional[LanguagesAccessData]


class TeamByProjectRole(TypedDict):
    name: TeamRole
    permissions: RolePermission
