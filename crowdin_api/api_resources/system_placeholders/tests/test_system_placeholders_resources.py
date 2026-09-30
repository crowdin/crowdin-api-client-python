from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.system_placeholders.enums import SystemPlaceholderPatchPath
from crowdin_api.api_resources.system_placeholders.resource import SystemPlaceholdersResource
from crowdin_api.requester import APIRequester


class TestSystemPlaceholdersResource:
    resource_class = SystemPlaceholdersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_get_system_placeholders_path(self, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_system_placeholders_path(projectId=1) == "projects/1/system-placeholders"

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"limit": 25, "offset": 0}),
            ({"limit": 10, "offset": 2}, {"limit": 10, "offset": 2}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_system_placeholders(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_system_placeholders(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/system-placeholders",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_system_placeholders_with_project_id(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=3
        )
        assert resource.list_system_placeholders() == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/3/system-placeholders",
            params={"limit": 25, "offset": 0},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_system_placeholders_batch_operations(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": SystemPlaceholderPatchPath.WRAPPED_AMPERSAND,
                "value": False,
            },
            {
                "op": PatchOperation.TEST,
                "path": SystemPlaceholderPatchPath.PRINTF_SPECIFIER,
                "value": True,
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.system_placeholders_batch_operations(projectId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="projects/1/system-placeholders",
            request_data=data,
        )
