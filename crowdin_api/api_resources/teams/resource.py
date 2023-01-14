from typing import Optional, Iterable

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.teams.types import Permissions, TeamPatchRequest, TeamByProjectRole


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

    def add_team_to_project(
        self,
        projectId: int,
        teamId: int,
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

    def list_teams(self, offset: Optional[int] = None, limit: Optional[int] = None):
        """
        List Teams.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_teams_path(),
            params=self.get_page_params(offset=offset, limit=limit),
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
