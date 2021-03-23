from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.string_comments.enums import (
    StringCommentIssueStatus,
    StringCommentIssueType,
    StringCommentType,
)
from crowdin_api.api_resources.string_comments.types import StringCommentPatchRequest


class StringCommentsResource(BaseResource):
    """
    Resource for String Comments.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/String-Comments
    """

    def get_string_comments_path(self, projectId: int, stringCommentId: Optional[int] = None):
        if stringCommentId is not None:
            return f"projects/{projectId}/comments/{stringCommentId}"

        return f"projects/{projectId}/comments"

    def list_string_comments(
        self,
        projectId: int,
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
        https://support.crowdin.com/api/v2/#operation/api.projects.comments.getMany
        """

        params = {
            "stringId": stringId,
            "type": type,
            "issueType": None if issueType is None else ",".join(item.value for item in issueType),
            "issueStatus": issueStatus,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_string_comments_path(projectId=projectId),
            params=params,
        )

    def add_string_comment(
        self,
        projectId: int,
        text: str,
        targetLanguageId: str,
        type: StringCommentType,
        issueType: Optional[StringCommentIssueType] = None,
    ):
        """
        Add String Comment.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.comments.post
        """

        return self.requester.request(
            method="post",
            path=self.get_string_comments_path(projectId=projectId),
            request_data={
                "text": text,
                "targetLanguageId": targetLanguageId,
                "type": type,
                "issueType": issueType,
            },
        )

    def get_string_comment(self, projectId: int, stringCommentId: int):
        """
        Get String Comment.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.comments.get
        """

        return self.requester.request(
            method="get",
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def delete_string_comment(self, projectId: int, stringCommentId: int):
        """
        Delete String Comment.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.comments.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def edit_string_comment(
        self,
        projectId: int,
        stringCommentId: int,
        data: Iterable[StringCommentPatchRequest],
    ):
        """
        Edit String Comment.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.comments.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )
