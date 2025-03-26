from typing import Optional, Iterable

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.teams.types \
    import Permissions, TeamPatchRequest, TeamByProjectRole, GroupTeamPatchRequest
from crowdin_api.api_resources.users.enums import ProjectRole
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_to_query_string, convert_enum_to_string_if_exists


class TeamsResource(BaseResource):
    """
    Resource for Teams.

    Organization teams.

    Use API to create, modify, and delete specific teams and members.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Teams
    """

    def get_teams_path(self, teamId: Optional[int] = None):
        if teamId is not None:
            return f"teams/{teamId}"

        return "teams"

    def get_members_path(self, teamId: int, memberId: Optional[int] = None):
        if memberId is not None:
            return f"teams/{teamId}/members/{memberId}"

        return f"teams/{teamId}/members"

    def get_group_teams_path(self, group_id: int, team_id: Optional[int] = None):
        if team_id is not None:
            return f"groups/{group_id}/teams/{team_id}"

        return f"groups/{group_id}/teams"

    def list_group_teams(
        self,
        group_id: int,
        order_by: Optional[Sorting] = None
    ):
        """
        List Group Teams

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Teams/operation/api.groups.teams.getMany
        """

        params = {
            "orderBy": order_by
        }

        return self.requester.request(
            method="get",
            path=self.get_group_teams_path(group_id),
            params=params
        )

    def update_group_teams(
        self,
        group_id: int,
        request_data: Iterable[GroupTeamPatchRequest]
    ):
        """
        Update Group Teams

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Teams/operation/api.groups.teams.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_group_teams_path(group_id),
            request_data=request_data
        )

    def get_group_team(
        self,
        group_id: int,
        team_id: int
    ):
        """
        Get Group Team

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Teams/operation/api.groups.teams.get
        """

        return self.requester.request(
            method="get",
            path=self.get_group_teams_path(group_id, team_id)
        )

    def add_team_to_project(
        self,
        teamId: int,
        projectId: Optional[int] = None,
        accessToAllWorkflowSteps: bool = True,
        managerAccess: bool = False,
        permissions: Optional[Permissions] = None,
        roles: Optional[Iterable[TeamByProjectRole]] = None
    ):
        """
        Add Team To Project.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.teams.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/teams",
            request_data={
                "teamId": teamId,
                "accessToAllWorkflowSteps": accessToAllWorkflowSteps,
                "managerAccess": managerAccess,
                "permissions": permissions,
                "roles": roles
            },
        )

    def list_teams(
        self,
        order_by: Optional[Sorting] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        project_ids: Optional[Iterable[int]] = None,
        project_roles: Optional[Iterable[ProjectRole]] = None,
        language_ids: Optional[Iterable[str]] = None,
        group_ids: Optional[Iterable[int]] = None,
    ):
        """
        List Teams.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.getMany
        """

        params = {
            "orderBy": order_by,
            "search": search,
            "projectIds": convert_to_query_string(project_ids, lambda project_id: str(project_id)),
            "projectRoles": convert_to_query_string(project_roles, lambda role: convert_enum_to_string_if_exists(role)),
            "languageIds": convert_to_query_string(language_ids, lambda language_id: str(language_id)),
            "groupIds": convert_to_query_string(group_ids, lambda group_id: str(group_id))
        }
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_teams_path(),
            params=params,
        )

    def add_team(self, name: str):
        """
        Add Team.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.post
        """

        return self.requester.request(
            method="post",
            path=self.get_teams_path(),
            request_data={"name": name}
        )

    def get_team(self, teamId: int):
        """
        Get Team.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.get
        """

        return self.requester.request(method="get", path=self.get_teams_path(teamId=teamId))

    def delete_team(self, teamId: int):
        """
        Delete Team.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.delete
        """

        return self.requester.request(method="delete", path=self.get_teams_path(teamId=teamId))

    def edit_team(self, teamId: int, data: Iterable[TeamPatchRequest]):
        """
        Edit Team.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_teams_path(teamId=teamId),
            request_data=data
        )

    def teams_member_list(
        self,
        teamId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        Team Members List.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.members.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_members_path(teamId=teamId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_team_members(self, teamId: int, userIds: Iterable[int]):
        """
        Add Team Members.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.members.post
        """

        return self.requester.request(
            method="post",
            path=self.get_members_path(teamId=teamId),
            request_data={"userIds": userIds},
        )

    def delete_all_team_members(self, teamId: int):
        """
        Delete All Team Members.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.members.deleteMany
        """

        return self.requester.request(method="delete", path=self.get_members_path(teamId=teamId))

    def delete_team_member(self, teamId: int, memberId: int):
        """
        Delete Team Member.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.members.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_members_path(teamId=teamId, memberId=memberId)
        )
