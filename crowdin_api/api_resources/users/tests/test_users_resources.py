from unittest import mock

import pytest
from crowdin_api.api_resources.users.enums import UserRole
from crowdin_api.api_resources.users.resource import UsersResource
from crowdin_api.requester import APIRequester


class TestUsersResource:
    resource_class = UsersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_authenticated_user(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_authenticated_user() == "response"
        m_request.assert_called_once_with(method="get", path="user")

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {},
                {
                    "search": None,
                    "role": None,
                    "languageId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "search": "search",
                    "role": UserRole.BLOCKED,
                    "languageId": "ua",
                    "offset": 0,
                    "limit": 25,
                },
                {
                    "search": "search",
                    "role": UserRole.BLOCKED,
                    "languageId": "ua",
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_members(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_project_members(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get", params=request_params, path="projects/1/members"
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_member_info(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_member_info(projectId=1, memberId=2) == "response"
        m_request.assert_called_once_with(method="get", path="projects/1/members/2")
