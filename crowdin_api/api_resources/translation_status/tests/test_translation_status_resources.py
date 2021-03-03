from unittest import mock

import pytest
from crowdin_api.api_resources.translation_status.enums import Category, Validation
from crowdin_api.api_resources.translation_status.resource import (
    TranslationStatusResource,
)
from crowdin_api.requester import APIRequester


class TestTranslationStatusResource:
    resource_class = TranslationStatusResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_branch_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_branch_progress(projectId=1, branchId=2, page=1) == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=1, offset=None, limit=None),
            path="projects/1/branches/2/languages/progress",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_directory_progress(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_directory_progress(projectId=1, directoryId=2, page=1)
            == "response"
        )
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
        assert (
            resource.get_language_progress(projectId=1, languageId="sr", page=1)
            == "response"
        )
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
            resource.get_project_progress(projectId=1, languageIds="sr,rs", page=1)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            params=params,
            path="projects/1/languages/progress",
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
                    "offset": 0,
                    "limit": 20,
                },
            ),
            (
                {
                    "languageIds": "some,string",
                    "category": [Category.ICU, Category.EMPTY],
                    "validation": [Validation.ICU_CHECK, Validation.TAGS_CHECK],
                },
                {
                    "languageIds": "some,string",
                    "category": "icu,empty",
                    "validation": "icu_check,tags_check",
                    "offset": 0,
                    "limit": 20,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_qa_check_issues(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_qa_check_issues(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get", path="projects/1/languages/progress", params=request_params
        )
