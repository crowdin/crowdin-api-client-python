from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.string_comments.enums import (
    StringCommentIssueStatus,
    StringCommentIssueType,
    StringCommentType,
)
from crowdin_api.api_resources.string_comments.types import StringCommentPatchRequest
from crowdin_api.sorting import Sorting


class StringCommentsResource(BaseResource):
    """
    Resource for String Comments.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/String-Comments
    """

    def get_string_comments_path(self, projectId: int, stringCommentId: Optional[int] = None):
        if stringCommentId is not None:
            return f"projects/{projectId}/comments/{stringCommentId}"

        return f"projects/{projectId}/comments"

    def list_string_comments(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        stringId: Optional[int] = None,
        type: Optional[StringCommentType] = None,
        issueType: Optional[Iterable[StringCommentIssueType]] = None,
        issueStatus: Optional[StringCommentIssueStatus] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List String Comments.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.comments.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "stringId": stringId,
            "type": type,
            "issueType": None if issueType is None else ",".join(item.value for item in issueType),
            "issueStatus": issueStatus,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_string_comments_path(projectId=projectId),
            params=params,
        )

    def add_string_comment(
        self,
        text: str,
        stringId: int,
        targetLanguageId: str,
        type: StringCommentType,
        projectId: Optional[int] = None,
        issueType: Optional[StringCommentIssueType] = None,
    ):
        """
        Add String Comment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.comments.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_string_comments_path(projectId=projectId),
            request_data={
                "text": text,
                "stringId": stringId,
                "targetLanguageId": targetLanguageId,
                "type": type,
                "issueType": issueType,
            },
        )

    def get_string_comment(self, stringCommentId: int, projectId: Optional[int] = None):
        """
        Get String Comment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.comments.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def delete_string_comment(
        self, stringCommentId: int, projectId: Optional[int] = None
    ):
        """
        Delete String Comment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.comments.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def edit_string_comment(
        self,
        stringCommentId: int,
        data: Iterable[StringCommentPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit String Comment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.comments.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )
