from unittest import mock

from crowdin_api.api_resources.organization.resource import OrganizationResource
from crowdin_api.requester import APIRequester


class TestOrganizationResource:
    resource_class = OrganizationResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_get_organization_path(self, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_path() == "organization"

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_organization(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization() == "response"
        m_request.assert_called_once_with(method="get", path="organization")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_organization_auth_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_auth_settings() == "response"
        m_request.assert_called_once_with(method="get", path="organization/auth-settings")
