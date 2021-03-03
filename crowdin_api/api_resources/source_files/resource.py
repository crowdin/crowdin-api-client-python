from typing import Any, List, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.source_files.enums import FileType, Priority
from crowdin_api.api_resources.source_files.types import (
    BranchPatchRequest,
    DirectoryPatchRequest,
    FilePatchRequest,
    GeneralExportOptions,
    OtherImportOptions,
    PropertyExportOptions,
    ReplaceFileFromStorageRequest,
    SpreadsheetImportOptions,
    XmlImportOptions,
)


class SourceFilesResource(BaseResource):
    """
    Resource for Source Files.

    Source files are resources for translation. You can keep files structure using folders or manage
    different versions of the content via branches.

    Use API to keep the source files up to date, check on file revisions, and manage project
    branches. Before adding source files to the project, upload each file to the Storage first.

    Note: If you use branches, make sure your master branch is the first one you integrate with
    Crowdin.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Source-Files
    """

    base_path = "projects"

    # Branches
    def get_branch_path(self, projectId: int, branchId: Optional[int] = None):
        if branchId is not None:
            return f"{self.prepare_path(projectId) }/branches/{branchId}"

        return f"{self.prepare_path(projectId) }/branches"

    def list_project_branches(
        self,
        projectId: int,
        name: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Branches.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.getMany
        """

        params = {"name": name}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get", path=self.get_branch_path(projectId=projectId), params=params
        )

    def add_branch(
        self,
        projectId: int,
        name: str,
        title: Optional[str] = None,
        exportPattern: Optional[str] = None,
        priority: Optional[Priority] = None,
    ):
        """
        Add Branch.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.post
        """

        return self.requester.request(
            method="post",
            path=self.get_branch_path(projectId=projectId),
            post_data={
                "name": name,
                "title": title,
                "exportPattern": exportPattern,
                "priority": priority,
            },
        )

    def get_branch(self, projectId: int, branchId: int):
        """
        Get Branch.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.get
        """

        return self.requester.request(
            method="get",
            path=self.get_branch_path(projectId=projectId, branchId=branchId),
        )

    def delete_branch(self, projectId: int, branchId: int):
        """
        Delete Branch.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.delete
        """

        return self.requester.request(
            method="delete",
            path=f"projects/{projectId}/branches/{branchId}",
        )

    def edit_branch(
        self, projectId: int, branchId: int, data: List[BranchPatchRequest]
    ):
        """
        Edit Branch.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_branch_path(projectId=projectId, branchId=branchId),
            post_data=data,
        )

    # Directories
    def get_directory_path(self, projectId: int, directoryId: Optional[int] = None):
        if directoryId is not None:
            return f"{self.prepare_path(projectId) }/directories/{directoryId}"

        return f"{self.prepare_path(projectId) }/directories"

    def list_directories(
        self,
        projectId: int,
        name: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Directories.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.branches.getMany
        """

        params = {"name": name}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_directory_path(projectId=projectId),
            params=params,
        )

    def add_directory(
        self,
        projectId: int,
        name: str,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        title: Optional[int] = None,
        exportPattern: Optional[str] = None,
        priority: Optional[Priority] = None,
    ):
        """
        Add Directory.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.directories.post
        """

        return self.requester.request(
            method="post",
            path=self.get_directory_path(projectId=projectId),
            post_data={
                "name": name,
                "branchId": branchId,
                "directoryId": directoryId,
                "title": title,
                "exportPattern": exportPattern,
                "priority": priority,
            },
        )

    def get_directory(self, projectId: int, directoryId: int):
        """
        Get Directory.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.directories.get
        """

        return self.requester.request(
            method="get",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
        )

    def delete_directory(self, projectId: int, directoryId: int):
        """
        Delete Directory.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.directories.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
        )

    def edit_directory(
        self, projectId: int, directoryId: int, data: List[DirectoryPatchRequest]
    ):
        """
        Edit Directory.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.directories.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
            post_data=data,
        )

    # Files
    def get_file_path(self, projectId: int, fileId: Optional[int] = None):
        if fileId is not None:
            return f"{self.prepare_path(projectId) }/files/{fileId}"

        return f"{self.prepare_path(projectId) }/files"

    def list_files(
        self,
        projectId: int,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        filter: Optional[str] = None,
        recursion: Any = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Files.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.getMany
        """

        params = {
            "branchId": branchId,
            "directoryId": directoryId,
            "filter": filter,
            "recursion": recursion,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get", path=self.get_file_path(projectId=projectId), params=params
        )

    def add_file(
        self,
        projectId: int,
        name: str,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        title: Optional[int] = None,
        type: Optional[FileType] = FileType.AUTO,
        importOptions: Optional[
            Union[SpreadsheetImportOptions, XmlImportOptions, OtherImportOptions]
        ] = None,
        exportOptions: Optional[
            Union[PropertyExportOptions, GeneralExportOptions]
        ] = None,
        excludedTargetLanguages: Optional[List[str]] = None,
        attachLabelIds: Optional[List[int]] = None,
    ):
        """
        Add File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.post
        """

        return self.requester.request(
            method="post",
            path=self.get_file_path(projectId=projectId),
            post_data={
                "name": name,
                "branchId": branchId,
                "directoryId": directoryId,
                "title": title,
                "type": type,
                "importOptions": importOptions,
                "exportOptions": exportOptions,
                "excludedTargetLanguages": excludedTargetLanguages,
                "attachLabelIds": attachLabelIds,
            },
        )

    def get_file(self, projectId: int, fileId: int):
        """
        Get File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.get
        """

        return self.requester.request(
            method="get",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
        )

    def update_or_restore_file(
        self, projectId: int, fileId: int, data: ReplaceFileFromStorageRequest
    ):
        """
        Update or Restore File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.put
        """

        return self.requester.request(
            method="put",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
            post_data=data,
        )

    def delete_file(self, projectId: int, fileId: int):
        """
        Delete File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
        )

    def edit_file(self, projectId: int, fileId: int, data: List[FilePatchRequest]):
        """
        Edit File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
            post_data=data,
        )

    def download_file(self, projectId: int, fileId: int):
        """
        Download File.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.download.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_file_path(projectId=projectId, fileId=fileId)}/download",
        )

    # File Revisions
    def get_file_revisions_path(
        self, projectId: int, fileId: int, revisionId: Optional[int] = None
    ):
        if revisionId is not None:
            return (
                f"{self.prepare_path(projectId)}/files/{fileId}/revisions/{revisionId}"
            )

        return f"{self.prepare_path(projectId)}/files/{fileId}/revisions"

    def list_file_revisions(
        self,
        projectId: int,
        fileId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List File Revisions.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.revisions.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_file_revisions_path(projectId=projectId, fileId=fileId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_file_revision(self, projectId: int, fileId: int, revisionId: int):
        """
        Get File Revision.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.files.revisions.get
        """

        return self.requester.request(
            method="get",
            path=self.get_file_revisions_path(
                projectId=projectId, fileId=fileId, revisionId=revisionId
            ),
        )
