from typing import Any, Optional, Iterable

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.users.enums import UserPatchPath, ProjectRole
from crowdin_api.typing import TypedDict


class UserPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: UserPatchPath


class LanguageData(TypedDict):
    allContent: bool
    workflowStepIds: Optional[Iterable[Any]]


class LanguagesAccessData(TypedDict):
    it: LanguageData
    uk: LanguageData


class RolePermission(TypedDict):
    allLanguages: bool
    languagesAccess: Optional[LanguagesAccessData]


class ProjectMemberRole(TypedDict):
    name: ProjectRole
    permissions: RolePermission
