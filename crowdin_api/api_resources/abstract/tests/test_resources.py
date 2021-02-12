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

        _resource = TestResource(requester=requester)

    @mock.patch("crowdin_api.requester.APIRequester")
    def test_prepare_path(self, base_absolut_url):
        class TestResource(BaseResource):
            base_path = "/test/"

        resource = TestResource(requester=APIRequester(base_url=base_absolut_url))

        assert resource.prepare_path(object_id=1) == "test/1"
        assert resource.prepare_path() == "test"
