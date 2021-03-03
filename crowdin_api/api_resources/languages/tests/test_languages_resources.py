from unittest import mock

import pytest
from crowdin_api.api_resources import LanguagesResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.languages.enums import (
    LanguagesPatchPath,
    LanguageTextDirection,
)
from crowdin_api.requester import APIRequester


class TestLanguagesResource:
    resource_class = LanguagesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_supported_languages(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_supported_languages(page=10) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=10, offset=None, limit=None),
            path="languages",
        )

    @pytest.mark.parametrize(
        "in_params, post_data",
        (
            (
                {
                    "name": "Some",
                    "code": "some",
                    "localeCode": "some-sm",
                    "textDirection": LanguageTextDirection.left_to_right,
                    "pluralCategoryNames": ["one"],
                },
                {
                    "name": "Some",
                    "code": "some",
                    "localeCode": "some-sm",
                    "textDirection": LanguageTextDirection.left_to_right,
                    "pluralCategoryNames": ["one"],
                    "twoLettersCode": None,
                    "dialectOf": None,
                },
            ),
            (
                {
                    "name": "Some",
                    "code": "some",
                    "localeCode": "some-sm",
                    "textDirection": LanguageTextDirection.left_to_right,
                    "pluralCategoryNames": ["one"],
                    "twoLettersCode": "sm",
                    "dialectOf": "uk",
                },
                {
                    "name": "Some",
                    "code": "some",
                    "localeCode": "some-sm",
                    "textDirection": LanguageTextDirection.left_to_right,
                    "pluralCategoryNames": ["one"],
                    "twoLettersCode": "sm",
                    "dialectOf": "uk",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_custom_language(
        self, m_request, in_params, post_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_custom_language(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post", path="languages", post_data=post_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_language(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_language(languageId=1) == "response"
        m_request.assert_called_once_with(method="get", path="languages/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_custom_language(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_custom_language(languageId=1) == "response"
        m_request.assert_called_once_with(method="delete", path="languages/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_custom_language(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": LanguagesPatchPath.name,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_custom_language(languageId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch", post_data=data, path="languages/1"
        )
