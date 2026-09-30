from typing import Any, Optional, Iterable

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.users.enums import (
    UserPatchPath,
    ProjectRole,
    AuthenticatedUserPatchPath,
)
from crowdin_api.typing import TypedDict


class UserPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: UserPatchPath


class AuthenticatedUserPatchRequest(TypedDict):
    value: str
    op: PatchOperation
    path: AuthenticatedUserPatchPath


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


class GroupManagerPatchRequest(TypedDict):
    op: PatchOperation
    path: str
    value: Any


class UserProjectPermissionsPatchRequest(TypedDict):
    """
    JSON Patch operation for project permissions.

    `path` is `/{projectId}/roles` (replace), `/{projectId}/roles/-` (add) or `/{projectId}` (remove).
    """

    op: PatchOperation
    path: str
    value: Any
