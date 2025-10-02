from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.task_comments.enums import TaskCommentPatchPath
from crowdin_api.api_resources.task_comments.resource import TaskCommentsResource
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting


class TestTaskCommentsResource:
    resource_class = TaskCommentsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1, "taskId": 2}, "projects/1/tasks/2/comments"),
            (
                {"projectId": 1, "taskId": 2, "taskCommentId": 3},
                "projects/1/tasks/2/comments/3",
            ),
        ),
    )
    def test_get_task_comments_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_comments_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"orderBy": None, "offset": 0, "limit": 25}),
            ({"orderBy": Sorting([])}, {"orderBy": Sorting([]), "offset": 0, "limit": 25}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_task_comments(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_task_comments(projectId=1, taskId=2, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_task_comments_path(projectId=1, taskId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_task_comment(projectId=1, taskId=2, text="hello") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_task_comments_path(projectId=1, taskId=2),
            request_data={"text": "hello"},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_comment(projectId=1, taskId=2, taskCommentId=3) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_task_comment(projectId=1, taskId=2, taskCommentId=3) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "new text",
                "op": PatchOperation.REPLACE,
                "path": TaskCommentPatchPath.TEXT,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_task_comment(projectId=1, taskId=2, taskCommentId=3, data=data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
            request_data=data,
        )


