from typing import Dict, Iterable, Optional, Union

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

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Projects

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
        hasManagerAccess: Optional[HasManagerAccess] = None,
    ):
        """
        List Projects.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.getMany
        """

        params = {"userId": userId, "hasManagerAccess": hasManagerAccess}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(method="get", path=self.get_projects_path(), params=params)

    def add_project(self, request_data: Dict):
        """
        Add Project.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.post
        """

        return self.requester.request(
            method="post", path=self.get_projects_path(), request_data=request_data
        )

    def add_file_based_project(
        self,
        name: str,
        sourceLanguageId: str,
        type: Optional[ProjectType] = None,
        normalizePlaceholder: Optional[bool] = None,
        saveMetaInfoInSource: Optional[bool] = None,
        identifier: Optional[str] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        visibility: Optional[ProjectVisibility] = None,
        languageAccessPolicy: Optional[ProjectLanguageAccessPolicy] = None,
        cname: Optional[str] = None,
        description: Optional[str] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
    ):
        """
        Add Project(Files Based Project Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.post
        """

        return self.add_project(
            request_data={
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

    def add_strings_based_project(
        self,
        name: str,
        sourceLanguageId: str,
        identifier: Optional[str] = None,
        type: Optional[ProjectType] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        visibility: Optional[ProjectVisibility] = None,
        languageAccessPolicy: Optional[ProjectLanguageAccessPolicy] = None,
        cname: Optional[str] = None,
        description: Optional[str] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
    ):
        """
        Add Project(Strings Based Project Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.post
        """

        return self.add_project(
            request_data={
                "name": name,
                "sourceLanguageId": sourceLanguageId,
                "identifier": identifier,
                "type": type,
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

    def get_project(self, projectId: int):
        """
        Get Project.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.get
        """

        return self.requester.request(
            method="get", path=self.get_projects_path(projectId=projectId)
        )

    def delete_project(self, projectId: int):
        """
        Delete Project.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.delete
        """

        return self.requester.request(
            method="delete", path=self.get_projects_path(projectId=projectId)
        )

    def edit_project(self, projectId: int, data: Iterable[ProjectPatchRequest]):
        """
        Edit Project.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_projects_path(projectId=projectId),
            request_data=data,
        )
