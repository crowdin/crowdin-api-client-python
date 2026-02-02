from unittest import mock

import pytest

from crowdin_api.api_resources.branches.enums import ListBranchesOrderBy, EditBranchPatchPath
from crowdin_api.api_resources.branches.resource import BranchesResource
from crowdin_api.api_resources.branches.types import CloneBranchRequest, AddBranchRequest, EditBranchPatch, \
    MergeBranchRequest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import SortingRule, Sorting, SortingOrder


class TestBranchesResource:
    resource_class = BranchesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_cloned_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2
        clone_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_cloned_branch(project_id, branch_id, clone_id) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=f"projects/{project_id}/branches/{branch_id}/clones/{clone_id}/branch",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                CloneBranchRequest(
                    name="Branch name",
                    title="Branch title"
                ),
                {
                    "name": "Branch name",
                    "title": "Branch title"
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clone_branch(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.clone_branch(project_id, branch_id, incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=f"projects/{project_id}/branches/{branch_id}/clones",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_branch_clone_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2
        clone_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_branch_clone_status(project_id, branch_id, clone_id)
        m_request.assert_called_once_with(
            method="get",
            path=f"projects/{project_id}/branches/{branch_id}/clones/{clone_id}",
        )

    @pytest.mark.parametrize(
        "in_params, query_params",
        (
            (
                {
                    "name": "My branch",
                    "order_by": Sorting(
                        [SortingRule(ListBranchesOrderBy.CREATED_AT, SortingOrder.DESC)]
                    ),
                    "limit": 10,
                    "offset": 2
                },
                {
                    "name": "My branch",
                    "orderBy": Sorting(
                        [SortingRule(ListBranchesOrderBy.CREATED_AT, SortingOrder.DESC)]
                    ),
                    "limit": 10,
                    "offset": 2
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_branches(self, m_request, in_params, query_params, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.list_branches(project_id=project_id, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=f"projects/{project_id}/branches",
            params=query_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                AddBranchRequest(
                    name="New branch",
                    title="Title of new branch"
                ),
                {
                    "name": "New branch",
                    "title": "Title of new branch"
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_branch(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.add_branch(project_id, incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=f"projects/{project_id}/branches",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.get_branch(project_id, branch_id) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=f"projects/{project_id}/branches/{branch_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_branch(project_id, branch_id) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=f"projects/{project_id}/branches/{branch_id}",
        )

    @pytest.mark.parametrize(
        "in_body, request_body",
        (
            (
                [
                    EditBranchPatch(
                        op=PatchOperation.REPLACE.value,
                        path=EditBranchPatchPath.NAME.value,
                        value="New name"
                    )
                ],
                [
                    {
                        "op": "replace",
                        "path": "/name",
                        "value": "New name"
                    }
                ]
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_branch(self, m_request, in_body, request_body, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_branch(project_id, branch_id, in_body) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=f"projects/{project_id}/branches/{branch_id}",
            request_data=request_body
        )

    @pytest.mark.parametrize(
        "in_data, request_data",
        (
            (
                MergeBranchRequest(
                    sourceBranchId=1,
                    deleteAfterMerge=True,
                    dryRun=True,
                    acceptSourceChanges=True
                ),
                {
                    "sourceBranchId": 1,
                    "deleteAfterMerge": True,
                    "dryRun": True,
                    "acceptSourceChanges": True
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_merge_branches(self, m_request, in_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        branch_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.merge_branch(project_id, branch_id, in_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"projects/{project_id}/branches/{branch_id}/merges",
            request_data=request_data,
        )
