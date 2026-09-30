from unittest import mock

import pytest

from crowdin_api.api_resources.custom_spellcheckers.resource import CustomSpellcheckersResource
from crowdin_api.requester import APIRequester


class TestCustomSpellcheckersResource:
    resource_class = CustomSpellcheckersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "custom-spellcheckers"),
            ({"customSpellcheckerId": 1}, "custom-spellcheckers/1"),
        ),
    )
    def test_get_custom_spellcheckers_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_custom_spellcheckers_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"offset": 0, "limit": 25}),
            ({"offset": 10, "limit": 5}, {"offset": 10, "limit": 5}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_custom_spellcheckers(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_custom_spellcheckers(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="custom-spellcheckers",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_custom_spellchecker(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_custom_spellchecker(customSpellcheckerId=1) == "response"
        m_request.assert_called_once_with(method="get", path="custom-spellcheckers/1")
