from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.project_placeholders.enums import (
    ProjectPlaceholderPatchPath,
    ProjectPlaceholderType,
)
from crowdin_api.api_resources.project_placeholders.resource import ProjectPlaceholdersResource
from crowdin_api.requester import APIRequester


class TestProjectPlaceholdersResource:
    resource_class = ProjectPlaceholdersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/placeholders"),
            ({"projectId": 1, "projectPlaceholderId": 2}, "projects/1/placeholders/2"),
        ),
    )
    def test_get_project_placeholders_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_project_placeholders_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"limit": 25, "offset": 0}),
            ({"limit": 10, "offset": 2}, {"limit": 10, "offset": 2}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_placeholders(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_project_placeholders(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/placeholders",
            params=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"customPlaceholderId": 3},
                {
                    "customPlaceholderId": 3,
                    "type": None,
                    "index": None,
                    "isBlocking": None,
                    "formats": None,
                },
            ),
            (
                {
                    "customPlaceholderId": 3,
                    "type": ProjectPlaceholderType.HIGH,
                    "index": 1,
                    "isBlocking": True,
                    "formats": ["docbook", "adoc"],
                },
                {
                    "customPlaceholderId": 3,
                    "type": ProjectPlaceholderType.HIGH,
                    "index": 1,
                    "isBlocking": True,
                    "formats": ["docbook", "adoc"],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_project_placeholder(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_project_placeholder(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/placeholders",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_project_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_project_placeholder(projectId=1, projectPlaceholderId=2) == "response"
        m_request.assert_called_once_with(method="get", path="projects/1/placeholders/2")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_project_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_project_placeholder(projectId=1, projectPlaceholderId=2) == "response"
        m_request.assert_called_once_with(method="delete", path="projects/1/placeholders/2")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_project_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": ProjectPlaceholderPatchPath.IS_BLOCKING,
                "value": True,
            },
            {
                "op": PatchOperation.REPLACE,
                "path": ProjectPlaceholderPatchPath.FORMATS,
                "value": ["adoc"],
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_project_placeholder(
            projectId=1, projectPlaceholderId=2, data=data
        ) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="projects/1/placeholders/2",
            request_data=data,
        )
