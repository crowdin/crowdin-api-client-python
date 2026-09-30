from datetime import datetime
from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.users.enums import UserRole, OrganizationRole, UserStatus
from crowdin_api.api_resources.users.types import (
    UserPatchRequest,
    ProjectMemberRole,
    GroupManagerPatchRequest,
    AuthenticatedUserPatchRequest,
    UserProjectPermissionsPatchRequest,
)
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_to_query_string, convert_enum_to_string_if_exists


class BaseUsersResource(BaseResource):
    """
    Base class with methods shared by `UsersResource` and `EnterpriseUsersResource`.
    """

    def get_authenticated_user(self):
        """
        Get Authenticated User.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.user.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.user.get
        """
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.getMany
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

    def get_member_info(self, memberId: int, projectId: Optional[int] = None):
        """
        Get Member Info.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.members.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_members_path(projectId=projectId, memberId=memberId)
        )

    def delete_member_from_project(
        self,
        memberId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Member From Project.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.members.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete", path=self.get_members_path(projectId=projectId, memberId=memberId)
        )


class UsersResource(BaseUsersResource):
    """
    Resource for Users.

    Users API gives you the possibility to get profile information about the currently
    authenticated user.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Users
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.getMany
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

    def edit_authenticated_user(self, data: Iterable[AuthenticatedUserPatchRequest]):
        """
        Edit Authenticated User.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.user.patch
        """

        return self.requester.request(method="patch", path="user", request_data=data)

    def add_project_member(
        self,
        userIds: Optional[Iterable[int]] = None,
        projectId: Optional[int] = None,
        usernames: Optional[Iterable[str]] = None,
        emails: Optional[Iterable[str]] = None,
        managerAccess: Optional[bool] = None,
        developerAccess: Optional[bool] = None,
        roles: Optional[Iterable[ProjectMemberRole]] = None,
        message: Optional[str] = None,
    ):
        """
        Add Project Member.

        One of `userIds`, `usernames` or `emails` is required.
        `managerAccess`, `developerAccess` and `roles` are mutually exclusive.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_members_path(projectId=projectId),
            request_data={
                "userIds": userIds,
                "usernames": usernames,
                "emails": emails,
                "managerAccess": managerAccess,
                "developerAccess": developerAccess,
                "roles": roles,
                "message": message,
            },
        )

    def replace_project_member_permissions(
        self,
        memberId: int,
        projectId: Optional[int] = None,
        managerAccess: Optional[bool] = None,
        developerAccess: Optional[bool] = None,
        roles: Optional[Iterable[ProjectMemberRole]] = None,
    ):
        """
        Replace Project Member Permissions.

        `managerAccess`, `developerAccess` and `roles` are mutually exclusive.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.members.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_members_path(projectId=projectId, memberId=memberId),
            request_data={
                "managerAccess": managerAccess,
                "developerAccess": developerAccess,
                "roles": roles,
            },
        )


class EnterpriseUsersResource(BaseUsersResource):
    """
    Resource for Enterprise platform Users.

    Users API gives you the possibility to get profile information about the currently
    authenticated user.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Users
    """
    def get_users_path(self, userId: Optional[int] = None):
        if userId is not None:
            return f"users/{userId}"

        return "users"

    def get_group_managers_path(self, group_id: int, user_id: Optional[int] = None):
        if user_id is not None:
            return f"groups/{group_id}/managers/{user_id}"

        return f"groups/{group_id}/managers"

    def list_group_managers(
        self,
        group_id: int,
        team_ids: Optional[Iterable[int]] = None,
        order_by: Optional[Sorting] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Group Managers

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Users/operation/api.groups.managers.getMany
        """

        params = {
            "teamIds": ",".join(str(teamId) for teamId in team_ids) if team_ids is not None else None,
            "orderBy": order_by
        }
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_group_managers_path(group_id),
            params=params
        )

    def update_group_managers(
        self,
        group_id: int,
        request_data: Iterable[GroupManagerPatchRequest]
    ):
        """
        Update Group Managers

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Users/operation/api.groups.managers.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_group_managers_path(group_id),
            request_data=request_data
        )

    def get_group_manager(
        self,
        group_id: int,
        user_id: int
    ):
        """
        Get Group Manager

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Users/operation/api.groups.managers.get
        """

        return self.requester.request(
            method="get",
            path=self.get_group_managers_path(group_id, user_id)
        )

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
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.members.getMany
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
        userIds: Optional[Iterable[int]] = None,
        projectId: Optional[int] = None,
        accessToAllWorkflowSteps: Optional[bool] = None,
        managerAccess: Optional[bool] = None,
        permissions: Optional[Dict] = None,
        roles: Optional[Iterable[ProjectMemberRole]] = None,
        usernames: Optional[Iterable[str]] = None,
        emails: Optional[Iterable[str]] = None,
        developerAccess: Optional[bool] = None,
    ):
        """
        Add Project Member.

        One of `userIds`, `usernames` or `emails` is required.

        `accessToAllWorkflowSteps` and `permissions` are deprecated by the API, use `roles` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.members.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_members_path(projectId=projectId),
            request_data={
                "userIds": userIds,
                "usernames": usernames,
                "emails": emails,
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "developerAccess": developerAccess,
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
        roles: Optional[Iterable[ProjectMemberRole]] = None,
        developerAccess: Optional[bool] = None,
    ):
        """
        Replace Project Member Permissions.

        `accessToAllWorkflowSteps` and `permissions` are deprecated by the API, use `roles` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.members.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_members_path(projectId=projectId, memberId=memberId),
            request_data={
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "developerAccess": developerAccess,
                "permissions": permissions,
                "roles": roles
            },
        )

    def invite_user(
        self,
        email: str,
        firstName: Optional[str] = None,
        lastName: Optional[str] = None,
        timezone: Optional[str] = None,
        adminAccess: Optional[bool] = None,
    ):
        """
        Invite User.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.post
        """
        return self.requester.request(
            method="post",
            path=self.get_users_path(),
            request_data={
                "email": email,
                "firstName": firstName,
                "lastName": lastName,
                "timezone": timezone,
                "adminAccess": adminAccess,
            }
        )

    def get_user(self, userId: int):
        """
        Get User.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.getById
        """

        return self.requester.request(method="get", path=self.get_users_path(userId=userId))

    def list_user_project_contributions(
        self,
        userId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List User Project Contributions.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.projects.contributions.getMany
        """

        return self._get_entire_data(
            method="get",
            path=f"{self.get_users_path(userId=userId)}/projects/contributions",
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def list_user_project_permissions(
        self,
        userId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List User Project Permissions.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.projects.permissions.getMany
        """

        return self._get_entire_data(
            method="get",
            path=f"{self.get_users_path(userId=userId)}/projects/permissions",
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def edit_user_project_permissions(
        self,
        userId: int,
        data: Iterable[UserProjectPermissionsPatchRequest],
    ):
        """
        Edit User Project Permissions.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.projects.permissions.patch
        """

        return self.requester.request(
            method="patch",
            path=f"{self.get_users_path(userId=userId)}/projects/permissions",
            request_data=data,
        )

    def edit_user(self, userId: int, data: Iterable[UserPatchRequest]):
        """
        Edit User.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.patch
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
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.users.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_users_path(userId=userId)
        )

    def list_users(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Sorting] = None,
        status: Optional[UserStatus] = None,
        search: Optional[str] = None,
        two_factor: Optional[str] = None,
        organization_roles: Optional[Iterable[OrganizationRole]] = None,
        team_id: Optional[int] = None,
        project_ids: Optional[Iterable[int]] = None,
        project_roles: Optional[Iterable[str]] = None,
        language_ids: Optional[Iterable[str]] = None,
        group_ids: Optional[Iterable[int]] = None,
        last_seen_from: Optional[datetime] = None,
        last_seen_to: Optional[datetime] = None
    ):
        """
        List Users

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Users/operation/api.users.getMany
        """

        params = {
            "limit": limit,
            "offset": offset,
            "orderBy": order_by,
            "status": convert_enum_to_string_if_exists(status),
            "search": search,
            "twoFactor": convert_enum_to_string_if_exists(two_factor),
            "organizationRoles": convert_to_query_string(
                organization_roles,
                lambda role: convert_enum_to_string_if_exists(role)
            ),
            "teamId": team_id,
            "projectIds": convert_to_query_string(project_ids, lambda project_id: str(project_id)),
            "projectRoles": convert_to_query_string(
                project_roles,
                lambda role: convert_enum_to_string_if_exists(role)
            ),
            "languageIds": convert_to_query_string(language_ids),
            "groupIds": convert_to_query_string(group_ids),
            "lastSeenFrom": last_seen_from.isoformat() if last_seen_from is not None else None,
            "lastSeenTo": last_seen_to.isoformat() if last_seen_to is not None else None
        }
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_users_path(),
            params=params
        )
