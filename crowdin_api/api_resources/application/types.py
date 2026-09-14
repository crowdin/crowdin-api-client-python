from typing import Any, Iterable, Optional

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.application.enums import (
    ApplicationConsentPatchPath,
    ApplicationConsentStatus,
    UserPermissions,
    ProjectPermissions,
)


class ApplicationUser(TypedDict):
    value: UserPermissions
    ids: Iterable[int]


class ApplicationProject(TypedDict):
    value: ProjectPermissions
    ids: Iterable[int]


class ApplicationPermissions(TypedDict):
    user: ApplicationUser
    project: ApplicationProject


class ApplicationInstallationPatchRequest(TypedDict):
    op: str
    path: str
    value: str


class AddApplicationConsentRequest(TypedDict):
    identifier: str
    installedBy: int
    status: ApplicationConsentStatus
    scopes: Optional[Iterable[str]]


class ApplicationConsentPatchRequest(TypedDict):
    op: PatchOperation
    path: ApplicationConsentPatchPath
    value: Any
