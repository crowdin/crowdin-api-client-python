from unittest import mock

import pytest

from crowdin_api import CrowdinClient


class TestCrowdinClient:
    @pytest.mark.parametrize(
        "http_protocol,organization,base_url,result",
        (
            (
                "http",
                None,
                "api.crowdin.com",
                "http://api.crowdin.com",
            ),
            (
                "https",
                None,
                "api.crowdin.com",
                "https://api.crowdin.com",
            ),
            (
                "http",
                "crowdin",
                "api.crowdin.com",
                "http://crowdin.api.crowdin.com",
            ),
            (
                "https",
                "crowdin",
                "api.crowdin.com",
                "https://crowdin.api.crowdin.com",
            ),
        ),
    )
    def test_url(self, http_protocol, organization, base_url, result):
        class TestClient(CrowdinClient):
            HTTP_PROTOCOL = http_protocol
            BASE_URL = base_url
            ORGANIZATION = organization

        assert TestClient().url == result

    @pytest.mark.parametrize(
        "headers,token,result",
        (
            (
                None,
                None,
                {
                    "Authorization": "Bearer None",
                    "User-Agent": "crowdin-api-client-python",
                },
            ),
            (
                {
                    "Authorization": "Same data",
                    "Some Header": "value",
                    "User-Agent": "crowdin-api-client-python-2",
                },
                "<token>",
                {
                    "Authorization": "Bearer <token>",
                    "Some Header": "value",
                    "User-Agent": "crowdin-api-client-python",
                },
            ),
        ),
    )
    def test_get_default_headers(self, headers, token, result):
        class TestClient(CrowdinClient):
            HEADERS = headers
            TOKEN = token

        assert TestClient().get_default_headers() == result

    @mock.patch("crowdin_api.client.CrowdinClient.API_REQUESTER_CLASS")
    def test_api_requestor(self, m_APIRequester):
        client = CrowdinClient()

        assert client._api_requestor is None
        first_api_requestor = client.get_api_requestor()
        assert client._api_requestor is not None
        second_api_requestor = client.get_api_requestor()
        assert first_api_requestor is second_api_requestor
        m_APIRequester.assert_called_once_with(
            base_url=client.url,
            timeout=client.TIMEOUT,
            default_headers=client.get_default_headers(),
        )

    @mock.patch("crowdin_api.client.StorageResource", return_value="StorageResource", autospec=True)
    @mock.patch("crowdin_api.client.CrowdinClient.get_api_requestor", return_value="api_requestor")
    def test_storages(self, _m_api_requestor, m_StorageResource):
        client = CrowdinClient()

        assert client.storages == "StorageResource"

        m_StorageResource.assert_called_once_with(requester="api_requestor")
