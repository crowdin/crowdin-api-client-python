from unittest import mock

import pytest
from crowdin_api.api_resources.enums import ExportFormat, PatchOperation
from crowdin_api.api_resources.translation_memory.enums import (
    ListTmSegmentsOrderBy,
    ListTmsOrderBy,
    TranslationMemoryPatchPath,
    TranslationMemorySegmentRecordOperation,
    TranslationMemorySegmentRecordOperationPath,
)
from crowdin_api.api_resources.translation_memory.resource import (
    TranslationMemoryResource,
)
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestTranslationMemoryResource:
    resource_class = TranslationMemoryResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

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

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTmsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "limit": 25,
                    "offset": 0,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTmsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "limit": 25,
                    "offset": 0,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tms(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_tms(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_tms_path(),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_tm(name="test", languageId="fr") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tms_path(),
            request_data={"name": "test", "languageId": "fr"},
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

    # TM Segments
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"tmId": 1}, "tms/1/segments"),
            ({"tmId": 1, "segmentId": 1}, "tms/1/segments/1"),
        ),
    )
    def test_get_tm_segments_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_tm_segments_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTmSegmentsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "limit": 25,
                    "offset": 0,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTmSegmentsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "limit": 25,
                    "offset": 0,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tm_segments(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_tm_segments(tmId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_tm_segments_path(1),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_tm_segment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        records = [
            {
                "languageId": "uk",
                "text": "Перекладений текст",
            }
        ]
        assert resource.create_tm_segment(1, records=records) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tm_segments_path(1),
            request_data={"records": records},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_tm_segment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_tm_segment(tmId=1, segmentId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_tm_segments_path(tmId=1, segmentId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_tm_segment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_tm_segment(tmId=1, segmentId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_tm_segments_path(tmId=1, segmentId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_tm_segment(
        self, m_request, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        data = [
            {
                "op": TranslationMemorySegmentRecordOperation.ADD,
                "path": TranslationMemorySegmentRecordOperationPath.ADD,
                "value": {
                    "text": "Перекладений текст",
                    "languageId": "uk",
                },
            }
        ]
        assert (
            resource.edit_tm_segment(tmId=1, segmentId=2, data=data) == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_tm_segments_path(tmId=1, segmentId=2),
            request_data=[
                {
                    "op": TranslationMemorySegmentRecordOperation.ADD,
                    "path": TranslationMemorySegmentRecordOperationPath.ADD,
                    "value": {
                        "text": "Перекладений текст",
                        "languageId": "uk",
                    }
                },
            ],
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
            method="post",
            path=resource.get_tm_export_path(tmId=1),
            request_data=request_data,
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

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_concordance_search_in_tms(self, m_reqeust, base_absolut_url):
        m_reqeust.return_value = "response"

        resource = self.get_resource(base_absolut_url)

        data = {
            "sourceLanguageId": "en",
            "targetLanguageId": "de",
            "autoSubstitution": True,
            "minRelevant": 60,
            "expressions": [
                "Welcome!",
                "Save as...",
                "View",
                "About..."
            ],
        }

        assert resource.concordance_search_in_tms(projectId=1, **data) == "response"
        m_reqeust.assert_called_once_with(
            method="post",
            path="projects/1/tms/concordance",
            request_data=data
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
