from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PluralCategoryName
from crowdin_api.api_resources.translation_status.enums import (
    Category,
    QaChecksRevalidationCategory,
    Validation,
)
from crowdin_api.api_resources.translation_status.resource import TranslationStatusResource
from crowdin_api.requester import APIRequester


class TestTranslationStatusResource:
    resource_class = TranslationStatusResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_branch_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_branch_progress(projectId=1, branchId=2, page=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=1, offset=None, limit=None),
            path="projects/1/branches/2/languages/progress",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_directory_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_directory_progress(projectId=1, directoryId=2, page=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=1, offset=None, limit=None),
            path="projects/1/directories/2/languages/progress",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_file_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_file_progress(projectId=1, fileId=2, page=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=1, offset=None, limit=None),
            path="projects/1/files/2/languages/progress",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_language_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_language_progress(projectId=1, languageId="sr", page=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=1, offset=None, limit=None),
            path="projects/1/languages/sr/progress",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_project_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)

        params = resource.get_page_params(page=1, offset=None, limit=None)
        params["languageIds"] = "sr,rs"

        assert (
            resource.get_project_progress(projectId=1, languageIds=["sr", "rs"], page=1)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            params=params,
            path="projects/1/languages/progress",
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {},
                {
                    "qaCheckCategories": None,
                    "languageIds": None,
                    "failedOnly": None,
                    "externalQaCheckIds": None,
                },
            ),
            (
                {
                    "qaCheckCategories": [QaChecksRevalidationCategory.AI],
                    "languageIds": ["uk", "fr"],
                    "failedOnly": True,
                    "externalQaCheckIds": [1, 2],
                },
                {
                    "qaCheckCategories": [QaChecksRevalidationCategory.AI],
                    "languageIds": ["uk", "fr"],
                    "failedOnly": True,
                    "externalQaCheckIds": [1, 2],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_start_qa_checks_revalidation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.start_qa_checks_revalidation(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/qa-checks/revalidate",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_qa_checks_revalidation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_qa_checks_revalidation_status(projectId=1, revalidationId="rev-id")
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/qa-checks/revalidate/rev-id",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_qa_checks_revalidation_status_without_id_is_deprecated(
        self, m_request, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        with pytest.warns(DeprecationWarning):
            assert resource.get_qa_checks_revalidation_status(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/qa-checks/revalidate",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_qa_checks_revalidation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.cancel_qa_checks_revalidation(projectId=1, revalidationId="rev-id")
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path="projects/1/qa-checks/revalidate/rev-id",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_qa_checks_revalidation_without_id_is_deprecated(
        self, m_request, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        with pytest.warns(DeprecationWarning):
            assert resource.cancel_qa_checks_revalidation(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path="projects/1/qa-checks/revalidate",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_validate_text_by_qa_checks(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {"stringId": 1, "languageId": "uk", "text": "text"},
            {
                "stringId": 2,
                "languageId": "uk",
                "text": "texts",
                "pluralCategoryName": PluralCategoryName.FEW,
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.validate_text_by_qa_checks(projectId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/translations/validate-qa-checks",
            request_data=data,
        )

    @pytest.mark.parametrize(
        "in_params,request_params",
        (
            (
                {},
                {
                    "languageIds": None,
                    "category": None,
                    "validation": None,
                    "taskId": None,
                    "fileId": None,
                    "branchId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "languageIds": ["some", "string"],
                    "category": [Category.ICU, Category.EMPTY],
                    "validation": [Validation.ICU_CHECK, Validation.TAGS_CHECK],
                },
                {
                    "languageIds": "some,string",
                    "category": "icu,empty",
                    "validation": "icu_check,tags_check",
                    "taskId": None,
                    "fileId": None,
                    "branchId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {"taskId": 1, "fileId": 2, "branchId": 3},
                {
                    "languageIds": None,
                    "category": None,
                    "validation": None,
                    "taskId": 1,
                    "fileId": 2,
                    "branchId": 3,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_qa_check_issues(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_qa_check_issues(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get", path="projects/1/qa-checks", params=request_params
        )
