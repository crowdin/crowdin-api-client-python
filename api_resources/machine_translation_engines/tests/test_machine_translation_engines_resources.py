from unittest import mock

import pytest

from crowdin_api.api_resources import MachineTranslationEnginesResource
from crowdin_api.requester import APIRequester


class TestTranslationMemoryResource:
    resource_class = MachineTranslationEnginesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "input_mtId, path",
        (
            (None, "mts"),
            (1, "mts/1"),
        ),
    )
    def test_get_mts_path(self, input_mtId, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_mts_path(mtId=input_mtId) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_mts(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_mts() == "response"
        m_request.assert_called_once_with(
            method="get",
            params={"offset": 0, "limit": 25},
            path=resource.get_mts_path(),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_tm(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_mt(mtId=1) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_mts_path(mtId=1)
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"mtId": 1, "targetLanguageId": "test"},
                {
                    "targetLanguageId": "test",
                    "languageRecognitionProvider": None,
                    "sourceLanguageId": None,
                    "strings": None,
                },
            ),
            (
                {
                    "mtId": 1,
                    "targetLanguageId": "test",
                    "languageRecognitionProvider": "crowdin",
                    "sourceLanguageId": "test",
                    "strings": ["test", "test"],
                },
                {
                    "targetLanguageId": "test",
                    "languageRecognitionProvider": "crowdin",
                    "sourceLanguageId": "test",
                    "strings": ["test", "test"],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_translate_via_mt(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.translate_via_mt(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_mts_path(mtId=1) + "/translations",
            request_data=request_data,
        )
