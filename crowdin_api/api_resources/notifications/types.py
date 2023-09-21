from typing import TypedDict, Iterable
from crowdin_api.api_resources.notifications.enums import MemberRole


class ByRoleRequestScehme(TypedDict):
    role: MemberRole
    message: str


class ByUserIdsRequestScheme(TypedDict):
    userIds: Iterable[int]
    message: str
