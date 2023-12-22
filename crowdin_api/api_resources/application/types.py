from typing import Iterable
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.application.enums import (
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
