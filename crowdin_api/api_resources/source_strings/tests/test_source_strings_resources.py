from unittest import mock

import pytest
from crowdin_api.api_resources.enums import DenormalizePlaceholders, PatchOperation
from crowdin_api.api_resources.source_strings.enums import (
    ListStringsOrderBy,
    ScopeFilter,
    SourceStringsPatchPath,
    StringBatchOperationsPath,
    StringBatchOperations,
    StringUpdateOption,
    UploadStringsType,
)
from crowdin_api.api_resources.source_strings.resource import (
    EnterpriseSourceStringsResource,
    SourceStringsResource,
)
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


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
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "filter": "filter",
                    "projectIds": None,
                    "userId": None,
                    "scope": None,
                    "denormalizePlaceholders": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "projectIds": [1, 2],
                    "userId": 3,
                    "scope": ScopeFilter.KEY,
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                    "offset": 5,
                    "limit": 10,
                },
                {
                    "filter": "filter",
                    "projectIds": "1,2",
                    "userId": 3,
                    "scope": ScopeFilter.KEY,
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                    "offset": 5,
                    "limit": 10,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_search_strings(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.search_strings(filter="filter", **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="strings",
        )

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
                    "orderBy": None,
                    "offset": 0,
                    "limit": 10,
                    "fileId": None,
                    "directoryId": None,
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
                    "orderBy": Sorting(
                        [SortingRule(ListStringsOrderBy.ID, SortingOrder.DESC)]
                    ),
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
                    "directoryId": 7,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListStringsOrderBy.ID, SortingOrder.DESC)]
                    ),
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
                    "directoryId": 7,
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
                    "branchId": None,
                    "fields": None,
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
                    "branchId": None,
                    "fields": {"some-field": "value"},
                },
                {
                    "text": "text",
                    "identifier": "identifier",
                    "fileId": 1,
                    "context": "context",
                    "isHidden": True,
                    "maxLength": 2,
                    "labelIds": [1, 2, 3],
                    "branchId": None,
                    "fields": {"some-field": "value"},
                },
            ),
            (
                {
                    "text": {"one": "string", "other": "strings"},
                    "identifier": "identifier",
                    "branchId": 3,
                },
                {
                    "text": {"one": "string", "other": "strings"},
                    "identifier": "identifier",
                    "fileId": None,
                    "context": None,
                    "isHidden": None,
                    "maxLength": None,
                    "labelIds": None,
                    "branchId": 3,
                    "fields": None,
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
            method="get",
            path=resource.get_source_strings_path(projectId=1, stringId=2),
            params={"denormalizePlaceholders": None},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_string_denormalize_placeholders(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_string(
                projectId=1,
                stringId=2,
                denormalizePlaceholders=DenormalizePlaceholders.ENABLE,
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_source_strings_path(projectId=1, stringId=2),
            params={"denormalizePlaceholders": DenormalizePlaceholders.ENABLE},
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
            params={"updateOption": None},
            path=resource.get_source_strings_path(projectId=1, stringId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_string_with_update_option(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "new.identifier",
                "op": PatchOperation.REPLACE,
                "path": SourceStringsPatchPath.IDENTIFIER,
            },
            {
                "value": {"some-field": "value"},
                "op": PatchOperation.REPLACE,
                "path": SourceStringsPatchPath.FIELDS,
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_string(
                projectId=1,
                stringId=2,
                data=data,
                updateOption=StringUpdateOption.KEEP_TRANSLATIONS,
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            params={"updateOption": StringUpdateOption.KEEP_TRANSLATIONS},
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
            params={"updateOption": None},
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_string_batch_operation_with_update_option(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": StringBatchOperations.ADD,
                "path": StringBatchOperationsPath.NEW_STRING,
                "value": {"text": "new", "identifier": "a.b.c", "branchId": 5},
            },
            {
                "op": StringBatchOperations.REMOVE,
                "path": StringBatchOperationsPath.STRING,
            },
        ]
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.string_batch_operation(
                projectId=1,
                data=data,
                updateOption=StringUpdateOption.CLEAR_TRANSLATIONS_AND_APPROVALS,
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_source_strings_path(1),
            params={"updateOption": StringUpdateOption.CLEAR_TRANSLATIONS_AND_APPROVALS},
            request_data=data,
        )

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/strings/uploads"),
            ({"projectId": 1, "uploadId": "abc"}, "projects/1/strings/uploads/abc"),
        ),
    )
    def test_get_strings_uploads_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_strings_uploads_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"storageId": 1, "branchId": 2},
                {
                    "storageId": 1,
                    "branchId": 2,
                    "type": None,
                    "parserVersion": None,
                    "labelIds": None,
                    "updateStrings": None,
                    "cleanupMode": None,
                    "importOptions": None,
                    "updateOption": None,
                },
            ),
            (
                {
                    "storageId": 1,
                    "branchId": 2,
                    "type": UploadStringsType.XLSX,
                    "parserVersion": 3,
                    "labelIds": [4, 5],
                    "updateStrings": True,
                    "cleanupMode": False,
                    "importOptions": {
                        "firstLineContainsHeader": True,
                        "scheme": {"identifier": 0, "sourcePhrase": 1},
                    },
                    "updateOption": StringUpdateOption.KEEP_TRANSLATIONS,
                },
                {
                    "storageId": 1,
                    "branchId": 2,
                    "type": UploadStringsType.XLSX,
                    "parserVersion": 3,
                    "labelIds": [4, 5],
                    "updateStrings": True,
                    "cleanupMode": False,
                    "importOptions": {
                        "firstLineContainsHeader": True,
                        "scheme": {"identifier": 0, "sourcePhrase": 1},
                    },
                    "updateOption": StringUpdateOption.KEEP_TRANSLATIONS,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_upload_strings(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.upload_strings(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/strings/uploads",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_upload_strings_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.upload_strings_status(projectId=1, uploadId="abc") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/strings/uploads/abc",
        )


class TestEnterpriseSourceStringsResource(TestSourceFilesResource):
    resource_class = EnterpriseSourceStringsResource

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/strings/reviewed-builds"),
            ({"projectId": 1, "buildId": 2}, "projects/1/strings/reviewed-builds/2"),
        ),
    )
    def test_get_reviewed_builds_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_reviewed_builds_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"branchId": None, "offset": 0, "limit": 25}),
            ({"branchId": 2, "offset": 5, "limit": 10}, {"branchId": 2, "offset": 5, "limit": 10}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_reviewed_source_files_builds(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_reviewed_source_files_builds(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/strings/reviewed-builds",
            params=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            ({}, {"branchId": None}),
            ({"branchId": 2}, {"branchId": 2}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_build_reviewed_source_files(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.build_reviewed_source_files(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/strings/reviewed-builds",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_reviewed_source_files_build_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.check_reviewed_source_files_build_status(projectId=1, buildId=2)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/strings/reviewed-builds/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_reviewed_source_files(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_reviewed_source_files(projectId=1, buildId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/strings/reviewed-builds/2/download",
        )
