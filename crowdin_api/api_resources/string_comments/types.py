from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.string_comments.enums import StringCommentPatchPath
from crowdin_api.typing import TypedDict


class StringCommentPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: StringCommentPatchPath
