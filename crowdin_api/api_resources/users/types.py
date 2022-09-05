from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.users.enums import UserPatchPath
from crowdin_api.typing import TypedDict


class UserPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: UserPatchPath
