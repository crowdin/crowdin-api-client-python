from typing import Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.string_comments.enums import (
    StringCommentIssueStatus,
    StringCommentIssueType,
    StringCommentType,
)
from crowdin_api.api_resources.string_comments.types import StringCommentPatchRequest, StringCommentBatchOpPatchRequest
from crowdin_api.sorting import Sorting


class StringCommentsResource(BaseResource):
    """
    Resource for String Comments.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/String-Comments
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
        fileId: Optional[int] = None,
    ):
        """
        List String Comments.

        :param stringId: Filter comments by string. Can't be used together with `fileId`.
        :param fileId: Filter comments by asset file (file-based projects only).
            Can't be used together with `stringId`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "stringId": stringId,
            "fileId": fileId,
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
        stringId: Optional[int] = None,
        targetLanguageId: Optional[str] = None,
        type: Optional[StringCommentType] = None,
        projectId: Optional[int] = None,
        issueType: Optional[StringCommentIssueType] = None,
        attachments: Optional[Iterable[Union[int, Dict[str, int]]]] = None,
        fileId: Optional[int] = None,
        isShared: Optional[bool] = None,
    ):
        """
        Add String Comment.

        :param stringId: String Identifier. Required unless `fileId` is used.
        :param type: Comment type (comment or issue). Required by the API.
        :param attachments: Storage Identifiers (or {"id": storageId} objects) of attachments.
        :param fileId: Asset File Identifier, used instead of `stringId` to comment
            an asset (file-based projects only).
        :param isShared: Defines shared comment or issue (Crowdin Enterprise only).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_string_comments_path(projectId=projectId),
            request_data={
                "text": text,
                "stringId": stringId,
                "fileId": fileId,
                "targetLanguageId": targetLanguageId,
                "type": type,
                "isShared": isShared,
                "issueType": issueType,
                "attachments": None
                if attachments is None
                else [
                    item if isinstance(item, dict) else {"id": item} for item in attachments
                ],
            },
        )

    def get_string_comment(self, stringCommentId: int, projectId: Optional[int] = None):
        """
        Get String Comment.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.get
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def delete_string_comment_attachment(
        self, stringCommentId: int, attachmentId: int, projectId: Optional[int] = None
    ):
        """
        Delete String Comment Attachment.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.attachments.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=(
                f"{self.get_string_comments_path(projectId=projectId, stringCommentId=stringCommentId)}"
                f"/attachments/{attachmentId}"
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.comments.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_string_comments_path(
                projectId=projectId, stringCommentId=stringCommentId
            ),
        )

    def string_comment_batch_operations(
        self,
        project_id: int,
        data: Iterable[StringCommentBatchOpPatchRequest]
    ):
        """
        String Comment Batch Operations.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/String-Comments/operation/api.projects.comments.batchPatch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Comments/operation/api.projects.comments.batchPatch
        """

        return self.requester.request(
            method="patch",
            path=f"projects/{project_id}/comments",
            request_data=data,
        )
