from unittest import mock

import pytest

from crowdin_api.api_resources.vendors.resource import VendorsResource
from crowdin_api.requester import APIRequester


class TestVendorsResources:
    resource_class = VendorsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_vendors(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_vendors(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="vendors",
            params=request_params,
        )
