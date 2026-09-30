from typing import Iterable

from crowdin_api.api_resources.notifications.enums import MemberRole, OrganizationMemberRole
from crowdin_api.typing import TypedDict


class ByRoleRequestScehme(TypedDict):
    role: MemberRole
    message: str


class ByUserIdsRequestScheme(TypedDict):
    userIds: Iterable[int]
    message: str


class ByOrganizationRoleRequestScheme(TypedDict):
    role: OrganizationMemberRole
    message: str
