from typing import Optional

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

    def get_member_info(self, projectId: int, memberId: int):
        """
        Get Member Info.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.members.get
        """

        return self.requester.request(method="get", path=f"projects/{projectId}/members/{memberId}")
