from unittest import mock

import pytest
from crowdin_api.api_resources.distributions.enums import DistributionPatchPath
from crowdin_api.api_resources.distributions.resource import DistributionsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester


class TestLanguagesResource:
    resource_class = DistributionsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/distributions"),
            ({"projectId": 1, "hash": "ua"}, "projects/1/distributions/ua"),
        ),
    )
    def test_get_distributions_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_distributions_path(**incoming_data) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_distributions(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_distributions(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(),
            path=resource.get_distributions_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_distribution(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_distribution(projectId=1, name="test", fileIds=[1, 2, 3]) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_distributions_path(projectId=1),
            request_data={"name": "test", "fileIds": [1, 2, 3]},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_distribution(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_distribution(projectId=1, hash="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_distributions_path(projectId=1, hash="hash")
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_distribution(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_distribution(projectId=1, hash="hash") == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_distributions_path(projectId=1, hash="hash"),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_distribution(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": DistributionPatchPath.TITLE,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_distribution(projectId=1, hash="hash", data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_distributions_path(projectId=1, hash="hash"),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_distribution_release(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_distribution_release(projectId=1, hash="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_distributions_path(projectId=1, hash="hash") + "/release",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_release_distribution(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.release_distribution(projectId=1, hash="hash") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_distributions_path(projectId=1, hash="hash") + "/release",
        )
