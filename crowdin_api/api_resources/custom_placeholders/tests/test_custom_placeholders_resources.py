from unittest import mock

import pytest

from crowdin_api.api_resources.custom_placeholders.enums import CustomPlaceholderPatchPath
from crowdin_api.api_resources.custom_placeholders.resource import CustomPlaceholdersResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester


class TestCustomPlaceholdersResource:
    resource_class = CustomPlaceholdersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "custom-placeholders"),
            ({"customPlaceholderId": 1}, "custom-placeholders/1"),
        ),
    )
    def test_get_custom_placeholders_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_custom_placeholders_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"offset": 0, "limit": 25}),
            ({"offset": 10, "limit": 5}, {"offset": 10, "limit": 5}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_custom_placeholders(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_custom_placeholders(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="custom-placeholders",
            params=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"definition": "start, then \"http\", end"},
                {
                    "definition": "start, then \"http\", end",
                    "description": None,
                    "argumentDelimiter": None,
                },
            ),
            (
                {
                    "definition": "start, then \"http\", end",
                    "description": "URL validation",
                    "argumentDelimiter": "'",
                },
                {
                    "definition": "start, then \"http\", end",
                    "description": "URL validation",
                    "argumentDelimiter": "'",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_custom_placeholder(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_custom_placeholder(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="custom-placeholders",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_custom_placeholder(customPlaceholderId=1) == "response"
        m_request.assert_called_once_with(method="get", path="custom-placeholders/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": CustomPlaceholderPatchPath.DESCRIPTION,
                "value": "test",
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert resource.edit_custom_placeholder(customPlaceholderId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="custom-placeholders/1",
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_custom_placeholder(customPlaceholderId=1) == "response"
        m_request.assert_called_once_with(method="delete", path="custom-placeholders/1")
