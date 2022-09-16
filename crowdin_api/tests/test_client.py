from unittest import mock

import pytest
from crowdin_api import CrowdinClient


class MockCrowdinClientEnterprise(CrowdinClient):
    ORGANIZATION = "TEST_COMPANY"


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

    @pytest.mark.parametrize(
        "property_name, class_name",
        (
            ("dictionaries", "DictionariesResource"),
            ("distributions", "DistributionsResource"),
            ("glossaries", "GlossariesResource"),
            ("labels", "LabelsResource"),
            ("languages", "LanguagesResource"),
            ("machine_translations", "MachineTranslationEnginesResource"),
            ("projects", "ProjectsResource"),
            ("reports", "ReportsResource"),
            ("screenshots", "ScreenshotsResource"),
            ("source_files", "SourceFilesResource"),
            ("source_strings", "SourceStringsResource"),
            ("storages", "StoragesResource"),
            ("string_comments", "StringCommentsResource"),
            ("string_translations", "StringTranslationsResource"),
            ("tasks", "TasksResource"),
            ("translation_memory", "TranslationMemoryResource"),
            ("translation_status", "TranslationStatusResource"),
            ("translations", "TranslationsResource"),
            ("users", "UsersResource"),
            ("webhooks", "WebhooksResource"),
        ),
    )
    @mock.patch(
        "crowdin_api.client.CrowdinClient.get_api_requestor",
        return_value="api_requestor",
    )
    def test_storages(self, _m_api_requestor, property_name, class_name):
        with mock.patch(
            f"crowdin_api.api_resources.{class_name}",
            return_value=class_name,
        ) as m_resource:
            client = CrowdinClient()
            assert getattr(client, property_name) == class_name
            m_resource.assert_called_once_with(requester="api_requestor", page_size=25)


class TestCrowdinClientEnterprise:
    @pytest.mark.parametrize(
        "property_name, class_name",
        (
            ("dictionaries", "DictionariesResource"),
            ("distributions", "DistributionsResource"),
            ("glossaries", "GlossariesResource"),
            ("groups", "GroupsResource"),
            ("labels", "LabelsResource"),
            ("languages", "LanguagesResource"),
            ("machine_translations", "MachineTranslationEnginesResource"),
            ("projects", "ProjectsResource"),
            ("reports", "EnterpriseReportsResource"),
            ("screenshots", "ScreenshotsResource"),
            ("source_files", "SourceFilesResource"),
            ("source_strings", "SourceStringsResource"),
            ("storages", "StoragesResource"),
            ("string_comments", "StringCommentsResource"),
            ("string_translations", "StringTranslationsResource"),
            ("tasks", "TasksResource"),
            ("teams", "TeamsResource"),
            ("translation_memory", "TranslationMemoryResource"),
            ("translation_status", "TranslationStatusResource"),
            ("translations", "TranslationsResource"),
            ("users", "EnterpriseUsersResource"),
            ("webhooks", "WebhooksResource"),
        ),
    )
    @mock.patch(
        "crowdin_api.client.CrowdinClient.get_api_requestor",
        return_value="api_requestor",
    )
    def test_storages_with_organization(self, _m_api_requestor, property_name, class_name):
        with mock.patch(
            f"crowdin_api.api_resources.{class_name}",
            return_value=class_name,
        ) as m_resource:
            client = MockCrowdinClientEnterprise()
            assert getattr(client, property_name) == class_name
            m_resource.assert_called_once_with(requester="api_requestor", page_size=25)
