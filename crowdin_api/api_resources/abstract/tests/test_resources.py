from unittest import mock

import pytest
from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.requester import APIRequester


class TestBaseResource:
    @mock.patch("crowdin_api.requester.APIRequester")
    def test_init(self, base_absolut_url):
        requester = APIRequester(base_url=base_absolut_url)
        with pytest.raises(TypeError):
            BaseResource(requester=requester)

        class TestResource(BaseResource):
            base_path = "test"

        _resource = TestResource(requester=requester)  # noqa F841

    @mock.patch("crowdin_api.requester.APIRequester")
    def test_prepare_path(self, base_absolut_url):
        class TestResource(BaseResource):
            base_path = "/test/"

        resource = TestResource(requester=APIRequester(base_url=base_absolut_url))

        assert resource.prepare_path(object_id=1) == "test/1"
        assert resource.prepare_path() == "test"

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
        class TestResource(BaseResource):
            base_path = "/test/"

        resource = TestResource(requester=APIRequester(base_url=base_absolut_url))

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
        class TestResource(BaseResource):
            base_path = "/test/"

        resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
        with pytest.raises(ValueError):
            resource.get_page_params(**kwargs)
