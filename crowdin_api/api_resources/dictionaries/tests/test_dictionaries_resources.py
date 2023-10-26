from unittest import mock

import pytest
from crowdin_api.api_resources.dictionaries.resource import DictionariesResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester


class TestDictionariesResource:
    resource_class = DictionariesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_project_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "languageIds": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {"languageIds": ["ua", "en", "pl"]},
                {
                    "languageIds": "ua,en,pl",
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_dictionaries(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_dictionaries(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="projects/1/dictionaries",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_custom_language(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": "/words/0",
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_dictionary(projectId=1, languageId="ua", data=data) == "response"
        m_request.assert_called_once_with(
            method="patch", request_data=data, path="projects/1/dictionaries/ua"
        )
