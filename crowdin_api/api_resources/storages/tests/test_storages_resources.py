from unittest import mock

from crowdin_api.api_resources import StorageResource
from crowdin_api.requester import APIRequester


class TestStorageResource:
    resource_class = StorageResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_storages(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_storages(page=10) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(page=10, offset=None, limit=None),
            path="storages",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_storage(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_storage("SOME_FILE") == "response"
        m_request.assert_called_once_with(
            method="post", path="storages", file="SOME_FILE"
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_storage(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_storage(storageId=1) == "response"
        m_request.assert_called_once_with(method="get", path="storages/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_storage(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_storage(storageId=1) == "response"
        m_request.assert_called_once_with(method="delete", path="storages/1")
