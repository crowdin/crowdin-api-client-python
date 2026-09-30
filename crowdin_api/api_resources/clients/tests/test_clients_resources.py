from unittest import mock

import pytest

from crowdin_api.api_resources.clients.resource import ClientsResource
from crowdin_api.requester import APIRequester


class TestClientsResource:
    resource_class = ClientsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_get_clients_path(self, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_clients_path() == "clients"

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"limit": 25, "offset": 0}),
            ({"limit": 10, "offset": 2}, {"limit": 10, "offset": 2}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_clients(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_clients(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="clients",
            params=request_params,
        )
