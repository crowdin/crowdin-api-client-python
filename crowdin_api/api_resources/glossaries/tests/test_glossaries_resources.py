from unittest import mock

import pytest
from crowdin_api.api_resources.enums import ExportFormat, PatchOperation
from crowdin_api.api_resources.glossaries.enums import (
    GlossaryPatchPath,
    TermPartOfSpeech,
    TermPatchPath,
)
from crowdin_api.api_resources.glossaries.resource import GlossariesResource
from crowdin_api.requester import APIRequester


class TestGlossariesResource:
    resource_class = GlossariesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    # Glossaries
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "glossaries/"),
            ({"glossaryId": 1}, "glossaries/1"),
        ),
    )
    def test_get_screenshots_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_glossaries_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_glossaries(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_glossaries() == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(),
            path=resource.get_glossaries_path(),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_glossary(name="test") == "response"
        m_request.assert_called_once_with(
            method="post", path=resource.get_glossaries_path(), request_data={"name": "test"}
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_glossary(glossaryId=1) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_glossaries_path(glossaryId=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_glossary(glossaryId=1) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_glossaries_path(glossaryId=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": GlossaryPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_glossary(glossaryId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch", request_data=data, path=resource.get_glossaries_path(glossaryId=1)
        )

    # Export
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"glossaryId": 1}, "glossaries/1/exports"),
            ({"glossaryId": 1, "exportId": 2}, "glossaries/1/exports/2"),
        ),
    )
    def test_get_glossary_export_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_glossary_export_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            ({}, {"format": None}),
            ({"format": ExportFormat.CSV}, {"format": ExportFormat.CSV}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_glossary(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_glossary(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path=resource.get_glossary_export_path(glossaryId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_glossary_export_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_glossary_export_status(glossaryId=1, exportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_glossary_export_path(glossaryId=1, exportId="hash")
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_glossary(glossaryId=1, exportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_glossary_export_path(glossaryId=1, exportId="hash") + "/download",
        )

    # Import
    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            ({"storageId": 1}, {"storageId": 1, "scheme": None, "firstLineContainsHeader": None}),
            (
                {"storageId": 1, "scheme": {}, "firstLineContainsHeader": True},
                {"storageId": 1, "scheme": {}, "firstLineContainsHeader": True},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_import_glossary(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.import_glossary(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path=resource.get_glossaries_path(glossaryId=1) + "/imports",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_glossary_import_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_glossary_import_status(glossaryId=1, importId="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_glossaries_path(glossaryId=1) + "/imports/hash"
        )

    # Terms
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"glossaryId": 1}, "glossaries/1/terms"),
            ({"glossaryId": 1, "termId": 2}, "glossaries/1/terms/2"),
        ),
    )
    def test_get_terms_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_terms_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "userId": None,
                    "languageId": None,
                    "translationOfTermId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "userId": 1,
                    "languageId": "ua",
                    "translationOfTermId": 2,
                },
                {
                    "userId": 1,
                    "languageId": "ua",
                    "translationOfTermId": 2,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_terms(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_terms(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_terms_path(glossaryId=1),
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {"languageId": "ua", "text": "text"},
                {
                    "languageId": "ua",
                    "text": "text",
                    "description": None,
                    "partOfSpeech": None,
                    "translationOfTermId": None,
                },
            ),
            (
                {
                    "languageId": "ua",
                    "text": "text",
                    "description": "description",
                    "partOfSpeech": TermPartOfSpeech.PARTICLE,
                    "translationOfTermId": 1,
                },
                {
                    "languageId": "ua",
                    "text": "text",
                    "description": "description",
                    "partOfSpeech": TermPartOfSpeech.PARTICLE,
                    "translationOfTermId": 1,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_term(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_term(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post", path=resource.get_terms_path(glossaryId=1), request_data=request_data
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {"languageId": None, "translationOfTermId": None},
            ),
            (
                {"languageId": "ua", "translationOfTermId": 1},
                {"languageId": "ua", "translationOfTermId": 1},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clear_glossary(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.clear_glossary(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_terms_path(glossaryId=1), params=request_params
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_term(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_term(glossaryId=1, termId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_terms_path(glossaryId=1, termId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_term(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_term(glossaryId=1, termId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_terms_path(glossaryId=1, termId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_term(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": TermPatchPath.TEXT,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_term(glossaryId=1, termId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch", request_data=data, path=resource.get_terms_path(glossaryId=1, termId=2)
        )
