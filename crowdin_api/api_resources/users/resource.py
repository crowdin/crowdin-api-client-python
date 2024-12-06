from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.users.enums import UserRole
from crowdin_api.api_resources.users.types import UserPatchRequest, ProjectMemberRole
from crowdin_api.sorting import Sorting


class BaseUsersResource(BaseResource):

    def get_authenticated_user(self):
        return self.requester.request(method="get", path="user")

    def get_members_path(self, projectId: int, memberId: Optional[int] = None):
        if memberId is not None:
            return f"projects/{projectId}/members/{memberId}"

        return f"projects/{projectId}/members"

    def _list_project_members(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        search: Optional[str] = None,
        languageId: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        extraParams: Optional[dict] = None
    ):
        """
        List Project Members.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.members.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"orderBy": orderBy, "search": search, "languageId": languageId}
        if extraParams:
            params.update(extraParams)

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

    def list_project_members(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
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
        """
        return self._list_project_members(
            projectId=projectId,
            orderBy=orderBy,
            search=search,
            languageId=languageId,
            page=page,
            offset=offset,
            limit=limit,
            extraParams={"role": role}
        )

    def get_member_info(self, memberId: int, projectId: Optional[int] = None):
        """
        Get Member Info.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.members.get
        """

        projectId = projectId or self.get_project_id()

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

    def list_project_members(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        search: Optional[str] = None,
        workflowStepId: Optional[int] = None,
        languageId: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Project Members.

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.getMany
        """

        return self._list_project_members(
            projectId=projectId,
            orderBy=orderBy,
            search=search,
            languageId=languageId,
            page=page,
            offset=offset,
            limit=limit,
            extraParams={"workflowStepId": workflowStepId}
        )

    def add_project_member(
        self,
        userIds: Iterable[int],
        projectId: Optional[int] = None,
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

        projectId = projectId or self.get_project_id()

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
        memberId: int,
        projectId: Optional[int] = None,
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

        projectId = projectId or self.get_project_id()

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
        memberId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Member From Project.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.members.delete
        """

        projectId = projectId or self.get_project_id()

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
