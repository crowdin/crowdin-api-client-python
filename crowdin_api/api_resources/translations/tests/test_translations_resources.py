from unittest import mock

import pytest
from crowdin_api.api_resources.enums import ExportProjectTranslationFormat
from crowdin_api.api_resources.translations.enums import (
    CharTransformation,
    PreTranslationApplyMethod,
    PreTranslationAutoApproveOption,
    PreTranslationEditOperation,
)
from crowdin_api.api_resources.translations.resource import TranslationsResource
from crowdin_api.requester import APIRequester


class TestTranslationsResource:
    resource_class = TranslationsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_branches(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.pre_translation_status(projectId=1, preTranslationId="2") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/pre-translations/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_pre_translations(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        params = resource.get_page_params()
        assert resource.list_pre_translations(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/pre-translations",
            params=params,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "languageIds": ["some", "language"],
                    "fileIds": [1, 2],
                },
                {
                    "languageIds": ["some", "language"],
                    "fileIds": [1, 2],
                    "method": None,
                    "engineId": None,
                    "aiPromptId": None,
                    "autoApproveOption": None,
                    "duplicateTranslations": None,
                    "skipApprovedTranslations": None,
                    "translateUntranslatedOnly": None,
                    "translateWithPerfectMatchOnly": None,
                    "fallbackLanguages": [],
                    "labelIds": [],
                    "excludeLabelIds": [],
                },
            ),
            (
                {
                    "languageIds": ["some", "language"],
                    "fileIds": [1, 2],
                    "method": PreTranslationApplyMethod.MT,
                    "engineId": 3,
                    "aiPromptId": 0,
                    "autoApproveOption": PreTranslationAutoApproveOption.ALL,
                    "duplicateTranslations": False,
                    "skipApprovedTranslations": False,
                    "translateUntranslatedOnly": False,
                    "translateWithPerfectMatchOnly": False,
                    "fallbackLanguages": ["lang"],
                    "labelIds": [1],
                    "excludeLabelIds": [1],
                },
                {
                    "languageIds": ["some", "language"],
                    "fileIds": [1, 2],
                    "method": PreTranslationApplyMethod.MT,
                    "engineId": 3,
                    "aiPromptId": 0,
                    "autoApproveOption": PreTranslationAutoApproveOption.ALL,
                    "duplicateTranslations": False,
                    "skipApprovedTranslations": False,
                    "translateUntranslatedOnly": False,
                    "translateWithPerfectMatchOnly": False,
                    "fallbackLanguages": ["lang"],
                    "labelIds": [1],
                    "excludeLabelIds": [1],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_apply_pre_translation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.apply_pre_translation(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path="projects/1/pre-translations",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "value",
                "op": PreTranslationEditOperation.REPLACE,
                "path": "/status",
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_pre_translation(projectId=1, preTranslationId="pre-id", data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="projects/1/pre-translations/pre-id",
            request_data=data,
        )

    @pytest.mark.parametrize(
        "in_params, request_data, headers",
        (
            (
                {"targetLanguageId": "some"},
                {
                    "targetLanguageId": "some",
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                },
                None,
            ),
            (
                {
                    "targetLanguageId": "some",
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": False,
                    "exportApprovedOnly": False,
                    "eTag": "eTag",
                },
                {
                    "targetLanguageId": "some",
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": False,
                    "exportApprovedOnly": False,
                },
                {"If-None-Match": "eTag"},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_build_project_file_translation(
        self, m_request, in_params, headers, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.build_project_file_translation(projectId=1, fileId=2, **in_params)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            headers=headers,
            path="projects/1/translations/builds/files/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_builds(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        params = resource.get_page_params()
        params["branchId"] = 2
        assert resource.list_project_builds(projectId=1, branchId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=params,
            path="projects/1/translations/builds",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_build_project_translation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.build_project_translation(projectId=1, request_data={"some_key": "some_value"})
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            request_data={"some_key": "some_value"},
            path=resource.get_builds_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {},
                {
                    "branchId": None,
                    "targetLanguageIds": None,
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                    "exportWithMinApprovalsCount": None,
                },
            ),
            (
                {
                    "branchId": 2,
                    "targetLanguageIds": ["ua", "en"],
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": False,
                    "exportWithMinApprovalsCount": True,
                },
                {
                    "branchId": 2,
                    "targetLanguageIds": ["ua", "en"],
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": False,
                    "exportWithMinApprovalsCount": True,
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.translations.resource."
        "TranslationsResource.build_project_translation"
    )
    def test_build_crowdin_project_translation(
        self, m_build_project_translation, in_params, request_data, base_absolut_url
    ):
        m_build_project_translation.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.build_crowdin_project_translation(projectId=1, **in_params) == "response"
        m_build_project_translation.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"pseudo": True},
                {
                    "pseudo": True,
                    "prefix": None,
                    "suffix": None,
                    "lengthTransformation": None,
                    "charTransformation": None,
                },
            ),
            (
                {
                    "pseudo": True,
                    "prefix": "python",
                    "suffix": "nohtyp",
                    "lengthTransformation": 2,
                    "charTransformation": CharTransformation.ARABIC,
                },
                {
                    "pseudo": True,
                    "prefix": "python",
                    "suffix": "nohtyp",
                    "lengthTransformation": 2,
                    "charTransformation": CharTransformation.ARABIC,
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.translations.resource."
        "TranslationsResource.build_project_translation"
    )
    def test_build_pseudo_project_translation(
        self, m_build_project_translation, in_params, request_data, base_absolut_url
    ):
        m_build_project_translation.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.build_pseudo_project_translation(projectId=1, **in_params) == "response"
        m_build_project_translation.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "storageId": 1,
                    "fileId": 2,
                },
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": None,
                    "autoApproveImported": None,
                    "translateHidden": None,
                    "addToTm": None,
                },
            ),
            (
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": False,
                    "autoApproveImported": False,
                    "translateHidden": False,
                    "addToTm": False,
                },
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": False,
                    "autoApproveImported": False,
                    "translateHidden": False,
                    "addToTm": False,
                },
            ),
            (
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": True,
                    "autoApproveImported": True,
                    "translateHidden": True,
                    "addToTm": True,
                },
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": True,
                    "autoApproveImported": True,
                    "translateHidden": True,
                    "addToTm": True,
                },
            ),
            (
                {
                    "storageId": 1,
                    "fileId": 2,
                    "addToTm": False,
                },
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": None,
                    "autoApproveImported": None,
                    "translateHidden": None,
                    "addToTm": False,
                },
            ),
            (
                {
                    "storageId": 1,
                    "fileId": 2,
                    "addToTm": True,
                },
                {
                    "storageId": 1,
                    "fileId": 2,
                    "importEqSuggestions": None,
                    "autoApproveImported": None,
                    "translateHidden": None,
                    "addToTm": True,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_upload_translation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.upload_translation(projectId=1, languageId="2", **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path="projects/1/translations/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_project_translations(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_project_translations(projectId=1, buildId="2") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/translations/builds/2/download",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_project_build_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_project_build_status(projectId=1, buildId="2") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/translations/builds/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_build(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.cancel_build(projectId=1, buildId="2") == "response"
        m_request.assert_called_once_with(
            method="delete",
            path="projects/1/translations/builds/2",
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "targetLanguageId": "ua",
                },
                {
                    "targetLanguageId": "ua",
                    "format": None,
                    "labelIds": None,
                    "branchIds": None,
                    "directoryIds": None,
                    "fileIds": None,
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                },
            ),
            (
                {
                    "targetLanguageId": "ua",
                    "format": ExportProjectTranslationFormat.MACOSX,
                    "labelIds": [1, 2, 3],
                    "branchIds": [4, 5, 6],
                    "directoryIds": [7, 8, 9],
                    "fileIds": [10, 11, 12],
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": False,
                },
                {
                    "targetLanguageId": "ua",
                    "format": ExportProjectTranslationFormat.MACOSX,
                    "labelIds": [1, 2, 3],
                    "branchIds": [4, 5, 6],
                    "directoryIds": [7, 8, 9],
                    "fileIds": [10, 11, 12],
                    "skipUntranslatedStrings": False,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": False,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_project_translation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_project_translation(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path="projects/1/translations/exports",
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "stringId": 1,
                    "languageId": "en",
                    "text": "translation",
                },
                {
                    "stringId": 1,
                    "languageId": "en",
                    "text": "translation",
                    "pluralCategoryName": None,
                    "addToTm": None,
                },
            ),
            (
                {
                    "stringId": 1,
                    "languageId": "en",
                    "text": "translation",
                    "pluralCategoryName": "one",
                    "addToTm": True,
                },
                {
                    "stringId": 1,
                    "languageId": "en",
                    "text": "translation",
                    "pluralCategoryName": "one",
                    "addToTm": True,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_translation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_translation(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data=request_data,
            path="projects/1/translations",
        )
