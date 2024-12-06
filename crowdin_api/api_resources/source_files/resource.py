from typing import Any, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.source_files.enums import (
    FileType,
    FileUpdateOption,
    Priority,
)
from crowdin_api.api_resources.source_files.types import (
    BranchPatchRequest,
    DirectoryPatchRequest,
    FilePatchRequest,
    GeneralExportOptions,
    JavascriptExportOptions,
    HtmlFileImportOptions,
    HtmlWithFrontMatterFileImportOptions,
    MdxV1FileImportOptions,
    MdxV2FileImportOptions,
    OtherImportOptions,
    PropertyExportOptions,
    SpreadsheetImportOptions,
    XmlImportOptions,
    DocxFileImportOptions,
)
from crowdin_api.sorting import Sorting


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
    https://developer.crowdin.com/api/v2/#tag/Source-Files
    """

    # Branches
    def get_branch_path(self, projectId: int, branchId: Optional[int] = None):
        if branchId is not None:
            return f"projects/{projectId}/branches/{branchId}"

        return f"projects/{projectId}/branches"

    def list_project_branches(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        name: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Branches.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"orderBy": orderBy, "name": name}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get", path=self.get_branch_path(projectId=projectId), params=params
        )

    def add_branch(
        self,
        name: str,
        projectId: Optional[int] = None,
        title: Optional[str] = None,
        exportPattern: Optional[str] = None,
        priority: Optional[Priority] = None,
    ):
        """
        Add Branch.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_branch_path(projectId=projectId),
            request_data={
                "name": name,
                "title": title,
                "exportPattern": exportPattern,
                "priority": priority,
            },
        )

    def get_branch(self, branchId: int, projectId: Optional[int] = None):
        """
        Get Branch.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_branch_path(projectId=projectId, branchId=branchId),
        )

    def delete_branch(self, branchId: int, projectId: Optional[int] = None):
        """
        Delete Branch.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=f"projects/{projectId}/branches/{branchId}",
        )

    def edit_branch(
        self,
        branchId: int,
        data: Iterable[BranchPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Branch.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_branch_path(projectId=projectId, branchId=branchId),
            request_data=data,
        )

    # Directories
    def get_directory_path(self, projectId: int, directoryId: Optional[int] = None):
        if directoryId is not None:
            return f"projects/{projectId}/directories/{directoryId}"

        return f"projects/{projectId}/directories"

    def list_directories(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        filter: Optional[str] = None,
        recursion=None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Directories.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "branchId": branchId,
            "directoryId": directoryId,
            "filter": filter,
            "recursion": recursion,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_directory_path(projectId=projectId),
            params=params,
        )

    def add_directory(
        self,
        name: str,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        title: Optional[int] = None,
        exportPattern: Optional[str] = None,
        priority: Optional[Priority] = None,
    ):
        """
        Add Directory.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_directory_path(projectId=projectId),
            request_data={
                "name": name,
                "branchId": branchId,
                "directoryId": directoryId,
                "title": title,
                "exportPattern": exportPattern,
                "priority": priority,
            },
        )

    def get_directory(self, directoryId: int, projectId: Optional[int] = None):
        """
        Get Directory.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
        )

    def delete_directory(self, directoryId: int, projectId: Optional[int] = None):
        """
        Delete Directory.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
        )

    def edit_directory(
        self,
        directoryId: int,
        data: Iterable[DirectoryPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Directory.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_directory_path(projectId=projectId, directoryId=directoryId),
            request_data=data,
        )

    # Files
    def get_file_path(self, projectId: int, fileId: Optional[int] = None):
        if fileId is not None:
            return f"projects/{projectId}/files/{fileId}"

        return f"projects/{projectId}/files"

    def list_files(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "branchId": branchId,
            "directoryId": directoryId,
            "filter": filter,
            "recursion": recursion,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get", path=self.get_file_path(projectId=projectId), params=params
        )

    def add_file(
        self,
        storageId: int,
        name: str,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        title: Optional[int] = None,
        context: Optional[str] = None,
        type: Optional[FileType] = FileType.AUTO,
        importOptions: Optional[
            Union[
                SpreadsheetImportOptions,
                XmlImportOptions,
                DocxFileImportOptions,
                OtherImportOptions,
                HtmlFileImportOptions,
                HtmlWithFrontMatterFileImportOptions,
                MdxV1FileImportOptions,
                MdxV2FileImportOptions,
            ]
        ] = None,
        exportOptions: Optional[
            Union[PropertyExportOptions, GeneralExportOptions, JavascriptExportOptions]
        ] = None,
        excludedTargetLanguages: Optional[Iterable[str]] = None,
        attachLabelIds: Optional[Iterable[int]] = None,
    ):
        """
        Add File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_file_path(projectId=projectId),
            request_data={
                "name": name,
                "storageId": storageId,
                "branchId": branchId,
                "directoryId": directoryId,
                "title": title,
                "type": type,
                "context": context,
                "importOptions": importOptions,
                "exportOptions": exportOptions,
                "excludedTargetLanguages": excludedTargetLanguages,
                "attachLabelIds": attachLabelIds,
            },
        )

    def get_file(self, fileId: int, projectId: Optional[int] = None):
        """
        Get File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
        )

    def restore_file(
        self, fileId: int, revisionId: int, projectId: Optional[int] = None
    ):
        """
        Restore File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
            request_data={"revisionId": revisionId},
        )

    def update_file(
        self,
        fileId: int,
        storageId: int,
        projectId: Optional[int] = None,
        updateOption: Optional[FileUpdateOption] = None,
        importOptions: Optional[
            Union[
                SpreadsheetImportOptions,
                XmlImportOptions,
                DocxFileImportOptions,
                OtherImportOptions,
                HtmlFileImportOptions,
                HtmlWithFrontMatterFileImportOptions,
                MdxV1FileImportOptions,
                MdxV2FileImportOptions,
            ]
        ] = None,
        exportOptions: Optional[
            Union[GeneralExportOptions, PropertyExportOptions, JavascriptExportOptions]
        ] = None,
        attachLabelIds: Optional[Iterable[int]] = None,
        detachLabelIds: Optional[Iterable[int]] = None,
    ):
        """
        Update File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
            request_data={
                "storageId": storageId,
                "updateOption": updateOption,
                "importOptions": importOptions,
                "exportOptions": exportOptions,
                "attachLabelIds": attachLabelIds,
                "detachLabelIds": detachLabelIds,
            },
        )

    def delete_file(self, fileId: int, projectId: Optional[int] = None):
        """
        Delete File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
        )

    def edit_file(
        self,
        fileId: int,
        data: Iterable[FilePatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_file_path(projectId=projectId, fileId=fileId),
            request_data=data,
        )

    def download_file_preview(self, fileId: int, projectId: Optional[int] = None):
        """
        Download File Preview.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.preview.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get", path=f"{self.get_file_path(projectId, fileId)}/preview"
        )

    def download_file(self, fileId: int, projectId: Optional[int] = None):
        """
        Download File.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.download.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"{self.get_file_path(projectId=projectId, fileId=fileId)}/download",
        )

    # File Revisions
    def get_file_revisions_path(
        self, projectId: int, fileId: int, revisionId: Optional[int] = None
    ):
        file_path = self.get_file_path(projectId=projectId, fileId=fileId)

        if revisionId is not None:
            return f"{file_path}/revisions/{revisionId}"

        return f"{file_path}/revisions"

    def list_file_revisions(
        self,
        fileId: int,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List File Revisions.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.revisions.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_file_revisions_path(projectId=projectId, fileId=fileId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_file_revision(
        self, fileId: int, revisionId: int, projectId: Optional[int] = None
    ):
        """
        Get File Revision.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.revisions.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_file_revisions_path(
                projectId=projectId, fileId=fileId, revisionId=revisionId
            ),
        )
