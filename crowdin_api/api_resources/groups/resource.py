from typing import Optional, Iterable

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.groups.types import GroupPatchRequest


class GroupsResource(BaseResource):
    """
    Resource for Groups.

    Groups allow you to organize your projects based on specific characteristics.
    Using projects, you can keep your source files sorted.

    Use API to manage projects and groups, change their settings, or remove them from
    organization if required.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Projects-and-Groups
    """

    # Glossaries
    def get_groups_path(self, groupId: Optional[int] = None):
        if groupId is not None:
            return f"groups/{groupId}"

        return "groups"

    def get_group(self, groupId: int):
        """
        Get Group.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.get
        """

        return self.requester.request(
            method="get",
            path=self.get_groups_path(groupId=groupId),
        )

    def add_group(
        self,
        name: str,
        parentId: Optional[int] = None,
        description: Optional[str] = None
    ):
        """
        Add Group.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.post
        """

        return self.requester.request(
            method="post",
            path=self.get_groups_path(),
            request_data={
                "name": name,
                "parentId": parentId,
                "description": description
            }
        )

    def list_groups(
        self,
        parentId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        """
        List Groups.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.getMany
        """

        params = {"parentId": parentId}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_groups_path(),
            params=params,
        )

    def edit_group(self, groupId: int, data: Iterable[GroupPatchRequest]):
        """
        Edit Group.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_groups_path(groupId=groupId),
            request_data=data,
        )

    def delete_group(self, groupId: int):
        """
        Delete Group.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_groups_path(groupId=groupId),
        )
