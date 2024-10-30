from unittest import mock

import pytest
from crowdin_api.api_resources.enums import DenormalizePlaceholders, PatchOperation
from crowdin_api.api_resources.source_strings.enums import (
    ScopeFilter,
    SourceStringsPatchPath,
    StringBatchOperationsPath,
    StringBatchOperations,
)
from crowdin_api.api_resources.source_strings.resource import SourceStringsResource
from crowdin_api.requester import APIRequester


class TestSourceFilesResource:
    resource_class = SourceStringsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/strings"),
            ({"projectId": 1, "stringId": 2}, "projects/1/strings/2"),
        ),
    )
    def test_get_source_strings_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_source_strings_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "fileId": None,
                    "croql": None,
                    "denormalizePlaceholders": None,
                    "labelIds": None,
                    "filter": None,
                    "scope": None,
                    "branchId": None,
                    "taskId": None,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "fileId": 1,
                    "croql": "croql",
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                    "labelIds": [1, 3, 4],
                    "filter": "some",
                    "scope": ScopeFilter.CONTEXT,
                    "branchId": 2,
                    "taskId": 5,
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "fileId": 1,
                    "croql": "croql",
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                    "labelIds": "1,3,4",
                    "filter": "some",
                    "scope": ScopeFilter.CONTEXT,
                    "branchId": 2,
                    "taskId": 5,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_strings(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_strings(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_source_strings_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "text": "text",
                },
                {
                    "text": "text",
                    "identifier": None,
                    "fileId": None,
                    "context": None,
                    "isHidden": None,
                    "maxLength": None,
                    "labelIds": None,
                    "branchId": None
                },
            ),
            (
                {
                    "text": "text",
                    "identifier": "identifier",
                    "fileId": 1,
                    "context": "context",
                    "isHidden": True,
                    "maxLength": 2,
                    "labelIds": [1, 2, 3],
                    "branchId": None
                },
                {
                    "text": "text",
                    "identifier": "identifier",
                    "fileId": 1,
                    "context": "context",
                    "isHidden": True,
                    "maxLength": 2,
                    "labelIds": [1, 2, 3],
                    "branchId": None
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_string(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_string(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_source_strings_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_string(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_string(projectId=1, stringId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_source_strings_path(projectId=1, stringId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_string(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_string(projectId=1, stringId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_source_strings_path(projectId=1, stringId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_string(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": SourceStringsPatchPath.TEXT,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_string(projectId=1, stringId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_source_strings_path(projectId=1, stringId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_string_batch_operation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": StringBatchOperations.REPLACE,
                "path": StringBatchOperationsPath.IS_HIDDEN,
                "value": True,
            },
            {
                "op": StringBatchOperations.REMOVE,
                "path": StringBatchOperationsPath.CONTEXT,
                "value": "some value",
            },
        ]
        resource = self.get_resource(base_absolut_url)
        assert resource.string_batch_operation(projectId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_source_strings_path(1),
            request_data=data,
        )
