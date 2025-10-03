from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.task_comments.types import TaskCommentPatchRequest
from crowdin_api.sorting import Sorting


class TaskCommentsResource(BaseResource):
    """
    Resource for Task Comments.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Tasks
    """

    def get_task_comments_path(
        self,
        projectId: int,
        taskId: int,
        taskCommentId: Optional[int] = None,
    ):
        if taskCommentId is not None:
            return f"projects/{projectId}/tasks/{taskId}/comments/{taskCommentId}"

        return f"projects/{projectId}/tasks/{taskId}/comments"

    def list_task_comments(
        self,
        taskId: int,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Task Comments.
        """

        projectId = projectId or self.get_project_id()
        params = {"orderBy": orderBy}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_task_comments_path(projectId=projectId, taskId=taskId),
            params=params,
        )

    def add_task_comment(
        self,
        text: str,
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Add Task Comment.
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_task_comments_path(projectId=projectId, taskId=taskId),
            request_data={"text": text},
        )

    def get_task_comment(
        self,
        taskCommentId: int,
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Get Task Comment.
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
        )

    def delete_task_comment(
        self,
        taskCommentId: int,
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Task Comment.
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
        )

    def edit_task_comment(
        self,
        taskCommentId: int,
        data: Iterable[TaskCommentPatchRequest],
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Edit Task Comment.
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
            request_data=data,
        )

