from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.users.enums import UserRole
from crowdin_api.api_resources.users.types import UserPatchRequest, ProjectMemberRole


class BaseUsersResource(BaseResource):

    def get_authenticated_user(self):
        return self.requester.request(method="get", path="user")

    def get_members_path(self, projectId: int, memberId: Optional[int] = None):
        if memberId is not None:
            return f"projects/{projectId}/members/{memberId}"

        return f"projects/{projectId}/members"

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
        https://developer.crowdin.com/api/v2/#operation/api.projects.members.getMany

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.getMany
        """

        params = {"search": search, "role": role, "languageId": languageId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_members_path(projectId=projectId),
            params=params,
        )


class UsersResource(BaseUsersResource):
    """
    Resource for Users.

    Users API gives you the possibility to get profile information about the currently
    authenticated user.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Users
    """

    def get_member_info(self, projectId: int, memberId: int):
        """
        Get Member Info.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.members.get
        """

        return self.requester.request(
            method="get",
            path=self.get_members_path(projectId=projectId, memberId=memberId)
        )


class EnterpriseUsersResource(BaseUsersResource):
    """
    Resource for Enterprise platform Users.

    Users API gives you the possibility to get profile information about the currently
    authenticated user.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Users
    """
    def get_users_path(self, userId: Optional[int] = None):
        if userId is not None:
            return f"users/{userId}"

        return "users"

    def add_project_member(
        self,
        projectId: int,
        userIds: Iterable[int],
        accessToAllWorkflowSteps: Optional[bool] = None,
        managerAccess: Optional[bool] = None,
        permissions: Optional[Dict] = None,
        roles: Optional[Iterable[ProjectMemberRole]] = None
    ):
        """
        Add Project Member.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.post
        """

        return self.requester.request(
            method="post",
            path=self.get_members_path(projectId=projectId),
            request_data={
                "userIds": userIds,
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "permissions": permissions,
                "roles": roles
            },
        )

    def replace_project_member_permissions(
        self,
        projectId: int,
        memberId: int,
        accessToAllWorkflowSteps: Optional[bool] = None,
        managerAccess: Optional[bool] = None,
        permissions: Optional[Dict] = None,
        roles: Optional[Iterable[ProjectMemberRole]] = None
    ):
        """
        Replace Project Member Permissions.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.put
        """

        return self.requester.request(
            method="put",
            path=self.get_members_path(projectId=projectId, memberId=memberId),
            request_data={
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "permissions": permissions,
                "roles": roles
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
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.delete
        """

        return self.requester.request(
            method="delete", path=self.get_members_path(projectId=projectId, memberId=memberId)
        )

    def invite_user(
        self,
        email: str,
        firstName: Optional[str] = None,
        lastName: Optional[str] = None,
        timezone: Optional[str] = None
    ):
        """
        Invite User.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.users.post
        """
        return self.requester.request(
            method="post",
            path=self.get_users_path(),
            request_data={
                "email": email,
                "firstName": firstName,
                "lastName": lastName,
                "timezone": timezone
            }
        )

    def edit_user(self, userId: int, data: Iterable[UserPatchRequest]):
        """
        Edit User.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.users.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_users_path(userId=userId),
            request_data=data
        )

    def delete_user(self, userId: int):
        """
        Delete User.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.users.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_users_path(userId=userId)
        )
