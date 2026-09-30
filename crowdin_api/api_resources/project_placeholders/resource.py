from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.project_placeholders.enums import ProjectPlaceholderType
from crowdin_api.api_resources.project_placeholders.types import ProjectPlaceholderPatchRequest


class ProjectPlaceholdersResource(BaseResource):
    """
    Resource for Project Placeholders.

    Custom placeholders of the organization assigned to a project. Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Placeholders
    """

    def get_project_placeholders_path(
        self, projectId: int, projectPlaceholderId: Optional[int] = None
    ):
        if projectPlaceholderId is not None:
            return f"projects/{projectId}/placeholders/{projectPlaceholderId}"

        return f"projects/{projectId}/placeholders"

    def list_project_placeholders(
        self,
        projectId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Project Placeholders.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.placeholders.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_project_placeholders_path(projectId=projectId),
            params=self.get_page_params(limit=limit, offset=offset),
        )

    def add_project_placeholder(
        self,
        customPlaceholderId: int,
        projectId: Optional[int] = None,
        type: Optional[ProjectPlaceholderType] = None,
        index: Optional[int] = None,
        isBlocking: Optional[bool] = None,
        formats: Optional[Iterable[str]] = None,
    ):
        """
        Add Project Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.placeholders.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_project_placeholders_path(projectId=projectId),
            request_data={
                "customPlaceholderId": customPlaceholderId,
                "type": type,
                "index": index,
                "isBlocking": isBlocking,
                "formats": formats,
            },
        )

    def get_project_placeholder(
        self, projectPlaceholderId: int, projectId: Optional[int] = None
    ):
        """
        Get Project Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.placeholders.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_project_placeholders_path(
                projectId=projectId, projectPlaceholderId=projectPlaceholderId
            ),
        )

    def delete_project_placeholder(
        self, projectPlaceholderId: int, projectId: Optional[int] = None
    ):
        """
        Delete Project Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.placeholders.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_project_placeholders_path(
                projectId=projectId, projectPlaceholderId=projectPlaceholderId
            ),
        )

    def edit_project_placeholder(
        self,
        projectPlaceholderId: int,
        data: Iterable[ProjectPlaceholderPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Project Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.placeholders.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_project_placeholders_path(
                projectId=projectId, projectPlaceholderId=projectPlaceholderId
            ),
            request_data=data,
        )
