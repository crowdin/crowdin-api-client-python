from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.task_comments.enums import TaskCommentPatchPath
from crowdin_api.typing import TypedDict


class TaskCommentPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TaskCommentPatchPath