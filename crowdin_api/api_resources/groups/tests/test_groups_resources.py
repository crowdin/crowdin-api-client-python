from unittest import mock

import pytest

from crowdin_api.api_resources import GroupsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.groups.enums import GroupPatchPath, ListGroupsOrderBy
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestGroupsResource:
    resource_class = GroupsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "groups"),
            ({"groupId": 1}, "groups/1"),
        ),
    )
    def test_get_groups_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_groups_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_group(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_group(groupId=1) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_groups_path(groupId=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_group(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_group(groupId=1) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_groups_path(groupId=1)
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "parentId": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListGroupsOrderBy.NAME, SortingOrder.DESC)]
                    ),
                    "parentId": "test",
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListGroupsOrderBy.NAME, SortingOrder.DESC)]
                    ),
                    "parentId": "test",
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_groups(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_groups(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_groups_path(),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {"name": "test_name"},
                {
                    "name": "test_name",
                    "parentId": None,
                    "description": None,
                },
            ),
            (
                {
                    "name": "test_name",
                    "parentId": 2,
                    "description": "some text",
                },
                {
                    "name": "test_name",
                    "parentId": 2,
                    "description": "some text",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_group(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_group(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_groups_path(),
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_group(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": GroupPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_group(groupId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_groups_path(groupId=1),
        )
