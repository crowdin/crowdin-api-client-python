from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.glossaries.enums import (
    GlossaryPatchPath,
    TermPartOfSpeech,
    TermPatchPath,
    TermStatus,
    TermType,
    TermGender,
    GlossaryFormat,
    GlossaryExportFields,
)
from crowdin_api.api_resources.glossaries.resource import GlossariesResource
from crowdin_api.requester import APIRequester


class TestGlossariesResource:
    resource_class = GlossariesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_project_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    # Glossaries
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "glossaries"),
            ({"glossaryId": 1}, "glossaries/1"),
        ),
    )
    def test_get_screenshots_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_glossaries_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "groupId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "groupId": 1,
                },
                {
                    "groupId": 1,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_glossaries(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_glossaries(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_glossaries_path(),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_glossary(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_glossary(name="test", languageId="fr") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_glossaries_path(),
            request_data={"name": "test", "languageId": "fr"},
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
            method="patch",
            request_data=data,
            path=resource.get_glossaries_path(glossaryId=1),
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
            (None, None),
            ({}, {}),
            (
                {
                    "format": GlossaryFormat.CSV,
                    "exportFields": [GlossaryExportFields.TERM, GlossaryExportFields.STATUS]
                },
                {
                    "format": GlossaryFormat.CSV,
                    "exportFields": [GlossaryExportFields.TERM, GlossaryExportFields.STATUS]
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_glossary(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_glossary(glossaryId=1, data=incoming_data) == "response"
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
            method="get",
            path=resource.get_glossary_export_path(glossaryId=1, exportId="hash"),
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
            (
                {"storageId": 1},
                {"storageId": 1, "scheme": None, "firstLineContainsHeader": None},
            ),
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
            method="get",
            path=resource.get_glossaries_path(glossaryId=1) + "/imports/hash",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_concordance_search_in_glossaries(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        data = {
            "sourceLanguageId": "es",
            "targetLanguageId": "de",
            "expressions": [
                "Welcome!",
                "Save as...",
                "View",
                "About...",
            ],
        }

        assert resource.concordance_search_in_glossaries(projectId=1, **data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/glossaries/concordance",
            request_data=data,
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
                    "conceptId": None,
                    "croql": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "userId": 1,
                    "languageId": "ua",
                    "conceptId": 2,
                    "croql": "status = 'preferred'",
                },
                {
                    "userId": 1,
                    "languageId": "ua",
                    "conceptId": 2,
                    "croql": "status = 'preferred'",
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
                    "status": None,
                    "type": None,
                    "gender": None,
                    "note": None,
                    "url": None,
                    "conceptId": None,
                },
            ),
            (
                {
                    "languageId": "ua",
                    "text": "text",
                    "description": "description",
                    "partOfSpeech": TermPartOfSpeech.PARTICLE,
                    "status": TermStatus.ADMITTED,
                    "type": TermType.SHORT_FORM,
                    "gender": TermGender.MASCULINE,
                    "note": "text",
                    "url": "https://test.test.com",
                    "conceptId": 1,
                },
                {
                    "languageId": "ua",
                    "text": "text",
                    "description": "description",
                    "partOfSpeech": TermPartOfSpeech.PARTICLE,
                    "status": TermStatus.ADMITTED,
                    "type": TermType.SHORT_FORM,
                    "gender": TermGender.MASCULINE,
                    "note": "text",
                    "url": "https://test.test.com",
                    "conceptId": 1,
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
            method="post",
            path=resource.get_terms_path(glossaryId=1),
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {"languageId": None, "conceptId": None},
            ),
            (
                {"languageId": "ua", "conceptId": 1},
                {"languageId": "ua", "conceptId": 1},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clear_glossary(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.clear_glossary(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_terms_path(glossaryId=1),
            params=request_params,
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
            method="patch",
            request_data=data,
            path=resource.get_terms_path(glossaryId=1, termId=2),
        )

    # Concepts
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"glossaryId": 1}, "glossaries/1/concepts"),
            ({"glossaryId": 1, "conceptId": 2}, "glossaries/1/concepts/2"),
        ),
    )
    def test_get_concepts_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_concepts_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_concepts(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_concepts(glossaryId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_concepts_path(glossaryId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_concept(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_concept(glossaryId=1, conceptId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_concepts_path(glossaryId=1, conceptId=2)
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "languagesDetails": [
                        {"languageId": "en", "definition": "This is a sample definition."}
                    ]
                },
                {
                    "languagesDetails": [
                        {"languageId": "en", "definition": "This is a sample definition."}
                    ],
                    "subject": None,
                    "definition": None,
                    "note": None,
                    "url": None,
                    "figure": None,
                },
            ),
            (
                {
                    "languagesDetails": [
                        {"languageId": "en", "definition": "This is a sample definition."}
                    ],
                    "subject": "general",
                    "definition": "This is a sample definition.",
                    "note": "Any concept-level note information",
                    "url": "https://test.test.com",
                    "figure": "string",
                },
                {
                    "languagesDetails": [
                        {"languageId": "en", "definition": "This is a sample definition."}
                    ],
                    "subject": "general",
                    "definition": "This is a sample definition.",
                    "note": "Any concept-level note information",
                    "url": "https://test.test.com",
                    "figure": "string",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_concept(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.update_concept(glossaryId=1, conceptId=2, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_concepts_path(glossaryId=1, conceptId=2),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_concept(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_concept(glossaryId=1, conceptId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_concepts_path(glossaryId=1, conceptId=2)
        )
