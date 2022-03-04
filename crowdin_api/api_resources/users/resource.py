from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.users.enums import UserRole


class UsersResource(BaseResource):
    """
    Resource for Users.

    Users API gives you the possibility to get profile information about the currently
    authenticated user.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Users
    """

    def get_authenticated_user(self):
        return self.requester.request(method="get", path="user")

    def list_project_members(
        self,
        projectId: int,
        search: Optional[str] = None,
        role: Optional[UserRole] = None,
        languageId: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Project Members.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.members.getMany
        """

        params = {"search": search, "role": role, "languageId": languageId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/members",
            params=params,
        )

    def add_project_member(
        self,
        projectId: int,
        userIds: Iterable[int],
        accessToAllWorkflowSteps: Optional[bool] = None,
        managerAccess: Optional[bool] = None,
        permissions: Optional[Dict] = None,
    ):
        """
        Add Project Member.

        Link to documentation:
        https://support.crowdin.com/enterprise/api/#operation/api.projects.members.post
        """

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/members",
            request_data={
                "userIds": userIds,
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "permissions": permissions,
            },
        )

    def replace_project_member_permissions(
        self,
        projectId: int,
        memberId: int,
        accessToAllWorkflowSteps: Optional[bool] = None,
        managerAccess: Optional[bool] = None,
        permissions: Optional[Dict] = None,
    ):
        """
        Replace Project Member Permissions.

        Link to documentation:
        https://support.crowdin.com/enterprise/api/#operation/api.projects.members.put
        """

        return self.requester.request(
            method="put",
            path=f"projects/{projectId}/members/{memberId}",
            request_data={
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "permissions": permissions,
            },
        )

    def delete_member_from_project(
        self,
        projectId: int,
        memberId: int,
    ):
        """
        Delete Member From Project.

        Link to documentation:
        https://support.crowdin.com/enterprise/api/#operation/api.projects.members.delete
        """

        return self.requester.request(
            method="delete", path=f"projects/{projectId}/members/{memberId}"
        )

    def get_member_info(self, projectId: int, memberId: int):
        """
        Get Member Info.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.members.get
        """

        return self.requester.request(method="get", path=f"projects/{projectId}/members/{memberId}")
