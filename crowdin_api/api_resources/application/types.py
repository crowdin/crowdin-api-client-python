from typing import Iterable
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.application.enums import (
    UserPermission,
    ProjectPermission,
)


class ApplicationUser(TypedDict):
    value: UserPermission
    ids: Iterable[int]


class ApplicationProject(TypedDict):
    value: ProjectPermission
    ids: Iterable[int]


class ApplicationPermissions(TypedDict):
    user: ApplicationUser
    project: ApplicationProject


class ApplicationInstallionPatchRequest(TypedDict):
    op: str
    path: str
    value: str
