from typing import Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.branches.types import (
    CloneBranchRequest,
    AddBranchRequest,
    EditBranchPatch,
    MergeBranchRequest
)
from crowdin_api.sorting import Sorting


class BranchesResource(BaseResource):
    """
    Resource for Branches.

    Branch CRUD and deletion status endpoints are available for both file-based and
    string-based projects. Clones and merges are available for string-based projects only.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Branches
    https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches

    Link to documentation for enterprise:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches
    https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches
    """

    def get_cloned_branch(
        self,
        project_id: int,
        branch_id: int,
        clone_id: str
    ):
        """
        Get Cloned Branch

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.branch.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.branch.get
        """

        return self.requester.request(
            method="get",
            path=f"projects/{project_id}/branches/{branch_id}/clones/{clone_id}/branch"
        )

    def get_branch_clones_path(self, project_id: int, branch_id: int, clone_id: Optional[str] = None):
        if clone_id is not None:
            return f"projects/{project_id}/branches/{branch_id}/clones/{clone_id}"
        return f"projects/{project_id}/branches/{branch_id}/clones"

    def clone_branch(
        self,
        project_id: int,
        branch_id: int,
        request_data: CloneBranchRequest
    ):
        """
        Clone Branch

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.post
        """

        return self.requester.request(
            method="post",
            path=self.get_branch_clones_path(project_id, branch_id),
            request_data=request_data
        )

    def check_branch_clone_status(
        self,
        project_id: int,
        branch_id: int,
        clone_id: str
    ):
        """
        Check Branch Clone Status

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.clones.get
        """

        return self.requester.request(
            method="get",
            path=self.get_branch_clones_path(project_id, branch_id, clone_id)
        )

    def get_branches_path(
        self,
        project_id: int,
        branch_id: Optional[int] = None
    ):
        if branch_id is not None:
            return f"projects/{project_id}/branches/{branch_id}"

        return f"projects/{project_id}/branches"

    def list_branches(
        self,
        project_id: int,
        name: Optional[str] = None,
        order_by: Optional[Sorting] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Branches

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.getMany
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.getMany
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.getMany
        """

        params = {
            "name": name,
            "orderBy": order_by,
        }
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get",
            path=self.get_branches_path(project_id),
            params=params,
        )

    def add_branch(
        self,
        project_id: int,
        request_data: AddBranchRequest
    ):
        """
        Add Branch

        `exportPattern` and `priority` are for file-based projects only,
        `isProtected` is for string-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.post
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.post
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.post
        """

        return self.requester.request(
            method="post",
            path=self.get_branches_path(project_id),
            request_data=request_data,
        )

    def get_branch(self, project_id: int, branch_id: int):
        """
        Get Branch

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.get
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.get
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.get
        """

        return self.requester.request(
            method="get",
            path=self.get_branches_path(project_id, branch_id),
        )

    def delete_branch(self, project_id: int, branch_id: int, prefer: Optional[str] = None):
        """
        Delete Branch

        Pass `prefer="respond-async"` to delete the branch asynchronously (recommended); the API
        then returns a job to poll via `check_branch_deletion_status`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.delete
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.delete
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.delete
        """

        headers = {"Prefer": prefer} if prefer is not None else None

        return self.requester.request(
            method="delete",
            headers=headers,
            path=self.get_branches_path(project_id, branch_id),
        )

    def check_branch_deletion_status(self, project_id: int, branch_id: int, job_identifier: str):
        """
        Check Branch Deletion Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.jobs.get
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.jobs.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.jobs.get
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.jobs.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_branches_path(project_id, branch_id)}/jobs/{job_identifier}",
        )

    def edit_branch(self, project_id: int, branch_id: int, patches: Iterable[EditBranchPatch]):
        """
        Edit Branch

        `/exportPattern` is for file-based projects only, `/isProtected` is for string-based
        projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Branches/operation/api.projects.branches.patch
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Branches/operation/api.projects.branches.patch
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_branches_path(project_id, branch_id),
            request_data=patches,
        )

    def get_branch_merges_path(self, project_id: int, branch_id: int, merge_id: Optional[Union[int, str]] = None):
        if merge_id is not None:
            return f"projects/{project_id}/branches/{branch_id}/merges/{merge_id}"

        return f"projects/{project_id}/branches/{branch_id}/merges"

    def merge_branch(self, project_id: int, branch_id: int, request: MergeBranchRequest):
        """
        Merge Branch

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.post
        """

        return self.requester.request(
            method="post",
            path=self.get_branch_merges_path(project_id, branch_id),
            request_data=request,
        )

    def check_branch_merge_status(self, project_id: int, branch_id: int, merge_id: Union[int, str]):
        """
        Check Branch Merge Status

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.get
        """

        return self.requester.request(
            method="get",
            path=self.get_branch_merges_path(project_id, branch_id, merge_id),
        )

    def get_branch_merge_summary(self, project_id: int, branch_id: int, merge_id: Union[int, str]):
        """
        Get Branch Merge Summary

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.summary.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#tag/Branches/operation/api.projects.branches.merges.summary.get
        """

        return self.requester.request(
            method="get",
            path=self.get_branch_merges_path(project_id, branch_id, merge_id) + "/summary",
        )
