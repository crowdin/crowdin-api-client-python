from unittest import mock

import pytest

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.users.enums import UserRole, UserPatchPath
from crowdin_api.api_resources.users.resource import (
    UsersResource,
    BaseUsersResource,
    EnterpriseUsersResource,
)
from crowdin_api.requester import APIRequester


class TestBaseUsersResource:
    resource_class = BaseUsersResource

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


class TestUsersResource:
    resource_class = UsersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "name_method",
        [
            "get_authenticated_user",
            "list_project_members",
            "get_member_info",
        ]
    )
    def test_present_methods(self, name_method):
        assert hasattr(self.resource_class, name_method)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_member_info(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_member_info(projectId=1, memberId=2) == "response"
        m_request.assert_called_once_with(method="get", path="projects/1/members/2")


class TestEnterpriseUsersResource:
    resource_class = EnterpriseUsersResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "name_method",
        [
            "get_authenticated_user",
            "get_users_path",
            "list_project_members",
            "add_project_member",
            "replace_project_member_permissions",
            "delete_member_from_project",
            "invite_user",
            "edit_user",
            "delete_user",
            "add_project_member",
            "replace_project_member_permissions",
            "delete_member_from_project",
        ]
    )
    def test_present_methods(self, name_method):
        assert hasattr(self.resource_class, name_method)

    @pytest.mark.parametrize(
        "userId, path",
        (
            (None, "users"),
            (1, "users/1"),
        ),
    )
    def test_get_users_path(self, userId, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_users_path(userId=userId) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"email": ""},
                {
                    "email": "",
                    "firstName": None,
                    "lastName": None,
                    "timezone": None
                },
            ),
            (
                {
                    "email": "john@example.com",
                    "firstName": "Jon",
                    "lastName": "Doe",
                    "timezone": "America/New_York"
                },
                {
                    "email": "john@example.com",
                    "firstName": "Jon",
                    "lastName": "Doe",
                    "timezone": "America/New_York"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_invite_user(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.invite_user(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post", path="users", request_data=request_params
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                [{
                    "value": 4,
                    "op": PatchOperation.REPLACE,
                    "path": UserPatchPath.FIRST_NAME
                }],
                [{
                    "value": 4,
                    "op": PatchOperation.REPLACE,
                    "path": UserPatchPath.FIRST_NAME
                }],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_user(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_user(userId=1, data=in_params) == "response"
        m_request.assert_called_once_with(
            method="patch", path="users/1", request_data=request_params
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_user(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_user(userId=1) == "response"
        m_request.assert_called_once_with(method="delete", path="users/1")
