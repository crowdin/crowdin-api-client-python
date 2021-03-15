from typing import List, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.projects.enums import (
    HasManagerAccess,
    ProjectLanguageAccessPolicy,
    ProjectType,
    ProjectVisibility,
)
from crowdin_api.api_resources.projects.types import ProjectPatchRequest


class ProjectsResource(BaseResource):
    """
    Resource for Storages.

    Using projects, you can keep your source files sorted.
    Use API to manage projects, change their settings, or remove them if required.

    Link to documentation: https://support.crowdin.com/api/v2/#tag/Projects

    """

    def get_projects_path(self, projectId: Optional[int] = None):
        if projectId is not None:
            return f"projects/{projectId}"

        return "projects"

    def list_projects(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        userId: Optional[Union[int, str]] = None,
        hasManagerAccess: HasManagerAccess = HasManagerAccess.FALSE,
    ):
        """
        List Projects.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.projects.getMany
        """

        params = {"userId": userId, "hasManagerAccess": hasManagerAccess}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get", path=self.get_projects_path(), params=params
        )

    def add_project(
        self,
        name: str,
        sourceLanguageId: str,
        identifier: Optional[str] = None,
        type: ProjectType = ProjectType.FILE_BASED,
        normalizePlaceholder: Optional[bool] = None,
        saveMetaInfoInSource: Optional[bool] = None,
        targetLanguageIds: Optional[List[str]] = None,
        visibility: ProjectVisibility = ProjectVisibility.PRIVATE,
        languageAccessPolicy: ProjectLanguageAccessPolicy = ProjectLanguageAccessPolicy.OPEN,
        cname: Optional[str] = None,
        description: Optional[str] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
    ):
        """
        Add Project.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.projects.post
        """

        return self.requester.request(
            method="post",
            path=self.get_projects_path(),
            post_data={
                "name": name,
                "sourceLanguageId": sourceLanguageId,
                "identifier": identifier,
                "type": type,
                "normalizePlaceholder": normalizePlaceholder,
                "saveMetaInfoInSource": saveMetaInfoInSource,
                "targetLanguageIds": targetLanguageIds,
                "visibility": visibility,
                "languageAccessPolicy": languageAccessPolicy,
                "cname": cname,
                "description": description,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
            },
        )

    def get_project(self, projectId):
        """
        Get Project.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.projects.get
        """

        return self.requester.request(
            method="get", path=self.get_projects_path(projectId=projectId)
        )

    def delete_project(self, projectId):
        """
        Delete Project.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.projects.delete
        """

        return self.requester.request(
            method="delete", path=self.get_projects_path(projectId=projectId)
        )

    def edit_project(self, projectId, data: List[ProjectPatchRequest]):
        """
        Edit Project.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.projects.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_projects_path(projectId=projectId),
            post_data=data,
        )
