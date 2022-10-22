from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.string_comments.enums import (
    StringCommentIssueStatus,
    StringCommentIssueType,
    StringCommentPatchPath,
    StringCommentType,
)
from crowdin_api.api_resources.string_comments.resource import StringCommentsResource
from crowdin_api.requester import APIRequester


class TestSourceFilesResource:
    resource_class = StringCommentsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/comments"),
            ({"projectId": 1, "stringCommentId": 2}, "projects/1/comments/2"),
        ),
    )
    def test_get_string_comments_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_string_comments_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": None,
                    "type": None,
                    "issueType": None,
                    "issueStatus": None,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "type": StringCommentType.COMMENT,
                    "issueType": [
                        StringCommentIssueType.CONTEXT_REQUEST,
                        StringCommentIssueType.SOURCE_MISTAKE,
                    ],
                    "issueStatus": StringCommentIssueStatus.UNRESOLVED,
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "type": StringCommentType.COMMENT,
                    "issueType": "context_request,source_mistake",
                    "issueStatus": StringCommentIssueStatus.UNRESOLVED,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_string_comments(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_string_comments(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_string_comments_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "text": "text",
                    "targetLanguageId": "ua",
                    "type": StringCommentType.COMMENT,
                },
                {
                    "text": "text",
                    "targetLanguageId": "ua",
                    "type": StringCommentType.COMMENT,
                    "issueType": None,
                },
            ),
            (
                {
                    "text": "text",
                    "targetLanguageId": "ua",
                    "type": StringCommentType.COMMENT,
                    "issueType": StringCommentIssueType.CONTEXT_REQUEST,
                },
                {
                    "text": "text",
                    "targetLanguageId": "ua",
                    "type": StringCommentType.COMMENT,
                    "issueType": StringCommentIssueType.CONTEXT_REQUEST,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_string_comment(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_string_comment(projectId=1, stringId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_string_comments_path(projectId=1, stringCommentId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_string_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_string_comment(projectId=1, stringCommentId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_string_comments_path(projectId=1, stringCommentId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_string_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_string_comment(projectId=1, stringCommentId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_string_comments_path(projectId=1, stringCommentId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_string_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": StringCommentPatchPath.TEXT,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_string_comment(projectId=1, stringCommentId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_string_comments_path(projectId=1, stringCommentId=2),
        )
