from unittest import mock

import pytest
from crowdin_api.api_resources.enums import ExportFormat, PatchOperation
from crowdin_api.api_resources.translation_memory.enums import TranslationMemoryPatchPath
from crowdin_api.api_resources.translation_memory.resource import TranslationMemoryResource
from crowdin_api.requester import APIRequester


class TestTranslationMemoryResource:
    resource_class = TranslationMemoryResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    # Translation Memory
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "tms"),
            ({"tmId": 1}, "tms/1"),
        ),
    )
    def test_get_screenshots_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_tms_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tms(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_tms() == "response"
        m_request.assert_called_once_with(
            method="get",
            params={"offset": 0, "limit": 25},
            path=resource.get_tms_path(),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_tm(name="test") == "response"
        m_request.assert_called_once_with(
            method="post", path=resource.get_tms_path(), request_data={"name": "test"}
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_tm(tmId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_tms_path(tmId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_tm(tmId=1) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_tms_path(tmId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "value",
                "op": PatchOperation.REPLACE,
                "path": TranslationMemoryPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_tm(tmId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch", path=resource.get_tms_path(tmId=1), request_data=data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clear_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.clear_tm(tmId=1) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_tms_path(tmId=1) + "/segments",
        )

    # Export
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"tmId": 1}, "tms/1/exports"),
            ({"tmId": 1, "exportId": "hash"}, "tms/1/exports/hash"),
        ),
    )
    def test_get_tm_export_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_tm_export_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {},
                {
                    "sourceLanguageId": None,
                    "targetLanguageId": None,
                    "format": None,
                },
            ),
            (
                {
                    "sourceLanguageId": "ua",
                    "targetLanguageId": "en",
                    "format": ExportFormat.CSV,
                },
                {
                    "sourceLanguageId": "ua",
                    "targetLanguageId": "en",
                    "format": ExportFormat.CSV,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_tm(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_tm(tmId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post", path=resource.get_tm_export_path(tmId=1), request_data=request_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_tm_export_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_tm_export_status(tmId=1, exportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_tm_export_path(tmId=1, exportId="hash"),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_tm(tmId=1, exportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_tm_export_path(tmId=1, exportId="hash") + "/download",
        )

    # Import
    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"storageId": 1},
                {
                    "storageId": 1,
                    "scheme": None,
                    "firstLineContainsHeader": None,
                },
            ),
            (
                {
                    "storageId": 1,
                    "scheme": {},
                    "firstLineContainsHeader": False,
                },
                {
                    "storageId": 1,
                    "scheme": {},
                    "firstLineContainsHeader": False,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_import_tm(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.import_tm(tmId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tms_path(tmId=1) + "/imports",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_tm_import_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_tm_import_status(tmId=1, importId="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_tms_path(tmId=1) + "/imports/hash"
        )
