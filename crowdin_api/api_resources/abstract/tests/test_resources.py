from unittest import mock
from unittest.mock import Mock

import pytest
from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.requester import APIRequester


class TestBaseResource:
    @pytest.mark.parametrize(
        "in_params,out_params",
        (
            ({}, {"limit": 25, "offset": 0}),
            ({"page": 1}, {"limit": 25, "offset": 0}),
            ({"page": 2}, {"limit": 25, "offset": 25}),
            ({"limit": 100, "offset": 0}, {"limit": 100, "offset": 0}),
        ),
    )
    def test_get_page_params_mixin(self, in_params, out_params, base_absolut_url):
        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))

        assert resource.get_page_params(**in_params) == out_params

    @pytest.mark.parametrize(
        "kwargs",
        (
            {"page": 1, "limit": 25, "offset": 0},
            {"page": -1},
            {"limit": -1, "offset": 0},
            {"limit": 25, "offset": -1},
        ),
    )
    def test_get_page_params_invalid_params(self, kwargs, base_absolut_url):
        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))
        with pytest.raises(ValueError):
            resource.get_page_params(**kwargs)

    @pytest.mark.parametrize(
        "in_param,out_param",
        (
            ({"max_limit": None}, None),
            ({"max_limit": 0}, 0),
            ({"max_limit": 1}, 1),
            ({"max_limit": 100}, 100),
        ),
    )
    def test_with_fetch_all(self, in_param, out_param, base_absolut_url):
        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))

        resource.with_fetch_all(**in_param)

        assert resource._max_limit == out_param
        assert resource._flag_fetch_all is True

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {"method": "get", "path": ""},
                {"method": "get", "path": "", "params": None},
            ),
            (
                {"method": "get", "path": "test", "params": "params"},
                {"method": "get", "path": "test", "params": "params"},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test__get_list(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))

        assert resource._get_entire_data(**incoming_data) == "response"
        m_request.assert_called_once_with(**request_data)

    @pytest.mark.parametrize(
        "max_limit, incoming_data, request_data",
        (
            (
                None,
                {"method": "get", "path": ""},
                {"method": "get", "path": "", "params": None, "max_amount": None},
            ),
            (
                0,
                {"method": "get", "path": "test", "params": "params"},
                {"method": "get", "path": "test", "params": "params", "max_amount": 0},
            ),
            (
                1,
                {"method": "get", "path": "test", "params": "params"},
                {"method": "get", "path": "test", "params": "params", "max_amount": 1},
            ),
        ),
    )
    def test__get_list_with__flag_fetch_all(
        self,
        incoming_data,
        max_limit,
        request_data,
        base_absolut_url
    ):
        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))
        resource.with_fetch_all(max_limit=max_limit)

        resource._fetch_all = Mock(return_value="response")

        assert resource._flag_fetch_all is True
        assert resource._get_entire_data(**incoming_data) == "response"
        assert resource._flag_fetch_all is False
        assert resource._max_limit is None
        resource._fetch_all.assert_called_once_with(**request_data)

    @pytest.mark.parametrize(
        "incoming_data, expected_result",
        (
            (
                {"method": "get", "path": ""},
                {"data": [None] * 1}
            ),
            (
                {"method": "get", "path": ""},
                {"data": [None] * 499}
            ),
            (
                {"method": "get", "path": "", "params": None, "max_amount": 0},
                {"data": []}
            ),
            (
                {"method": "get", "path": "", "params": None, "max_amount": 1},
                {"data": [None] * 1}
            ),
            (
                {"method": "get", "path": "", "params": None, "max_amount": 499},
                {"data": [None] * 499}
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test__fetch_all(self, m_request, incoming_data, expected_result, base_absolut_url):
        m_request.return_value = expected_result
        resource = BaseResource(requester=APIRequester(base_url=base_absolut_url))

        testing_result = resource._fetch_all(**incoming_data)
        assert testing_result == expected_result
