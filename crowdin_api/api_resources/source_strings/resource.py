from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders
from crowdin_api.api_resources.source_strings.enums import (
    ScopeFilter,
    StringUpdateOption,
    UploadStringsType,
)
from crowdin_api.api_resources.source_strings.types import (
    SourceStringsPatchRequest,
    StringBatchOperationPatchRequest,
    UploadStringsImportOptions,
)
from crowdin_api.sorting import Sorting


class SourceStringsResource(BaseResource):
    """
    Resource for Source Strings.

    Source strings are the text units for translation. Instead of modifying source files,
    you can manage source strings one by one.

    Use API to add, edit, or delete some specific strings in the source-based and files-based
    projects (available only for the following file formats: CSV, RESX, JSON, Android XML,
    iOS strings, PROPERTIES, XLIFF).

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Source-Strings
    """

    def search_strings(
        self,
        filter: str,
        projectIds: Optional[Iterable[int]] = None,
        userId: Optional[int] = None,
        scope: Optional[ScopeFilter] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Search Strings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.strings.getMany
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.strings.getMany
        """

        params = {
            "filter": filter,
            "projectIds": None
            if projectIds is None
            else ",".join(str(projectId) for projectId in projectIds),
            "userId": userId,
            "scope": scope,
            "denormalizePlaceholders": denormalizePlaceholders,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path="strings", params=params)

    def get_source_strings_path(self, projectId: int, stringId: Optional[int] = None):
        if stringId is not None:
            return f"projects/{projectId}/strings/{stringId}"

        return f"projects/{projectId}/strings"

    def list_strings(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        fileId: Optional[int] = None,
        branchId: Optional[int] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        labelIds: Optional[Iterable[int]] = None,
        taskId: Optional[int] = None,
        croql: Optional[str] = None,
        filter: Optional[str] = None,
        scope: Optional[ScopeFilter] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        directoryId: Optional[int] = None,
    ):
        """
        List Strings.

        :param directoryId: Directory Identifier (file-based projects only).
            Can't be used with `taskId`, `fileId` or `branchId` in the same request.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "branchId": branchId,
            "fileId": fileId,
            "directoryId": directoryId,
            "denormalizePlaceholders": denormalizePlaceholders,
            "labelIds": None if labelIds is None else ",".join(str(item) for item in labelIds),
            "taskId": taskId,
            "filter": filter,
            "croql": croql,
            "scope": scope,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_source_strings_path(projectId=projectId),
            params=params,
        )

    def add_string(
        self,
        text: Union[str, Dict[str, str]],
        projectId: Optional[int] = None,
        identifier: Optional[str] = None,
        fileId: Optional[int] = None,
        context: Optional[str] = None,
        isHidden: Optional[bool] = None,
        maxLength: Optional[int] = None,
        labelIds: Optional[Iterable[int]] = None,
        branchId: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add String.

        :param text: Text for translation. Use a dict (e.g. {"one": "...", "other": "..."})
            for plural strings.
        :param fileId: File Identifier (file-based projects only).
        :param branchId: Branch Identifier (string-based projects only).
        :param fields: Fields values, keys get via List Fields (Crowdin Enterprise only).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_source_strings_path(projectId=projectId),
            request_data={
                "text": text,
                "identifier": identifier,
                "fileId": fileId,
                "context": context,
                "isHidden": isHidden,
                "maxLength": maxLength,
                "labelIds": labelIds,
                "branchId": branchId,
                "fields": fields,
            },
        )

    def get_string(
        self,
        stringId: int,
        projectId: Optional[int] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
    ):
        """
        Get String.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
            params={"denormalizePlaceholders": denormalizePlaceholders},
        )

    def delete_string(self, stringId: int, projectId: Optional[int] = None):
        """
        Delete String.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
        )

    def edit_string(
        self,
        stringId: int,
        data: Iterable[SourceStringsPatchRequest],
        projectId: Optional[int] = None,
        updateOption: Optional[StringUpdateOption] = None,
    ):
        """
        Edit String.

        :param updateOption: Defines whether to keep existing translations and approvals for
            the updated string. Applied only when `text` or `identifier` is changed.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
            params={"updateOption": updateOption},
            request_data=data,
        )

    def string_batch_operation(
        self,
        data: Iterable[StringBatchOperationPatchRequest],
        projectId: Optional[int] = None,
        updateOption: Optional[StringUpdateOption] = None,
    ):
        """
        String Batch Operations.

        :param updateOption: Defines whether to keep existing translations and approvals for
            updated strings. Applied only when `text` or `identifier` is changed.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings.batchPatch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_source_strings_path(projectId=projectId),
            params={"updateOption": updateOption},
            request_data=data,
        )

    # Upload Strings
    def get_strings_uploads_path(self, projectId: int, uploadId: Optional[str] = None):
        if uploadId is not None:
            return f"projects/{projectId}/strings/uploads/{uploadId}"

        return f"projects/{projectId}/strings/uploads"

    def upload_strings(
        self,
        storageId: int,
        branchId: int,
        projectId: Optional[int] = None,
        type: Optional[UploadStringsType] = None,
        parserVersion: Optional[int] = None,
        labelIds: Optional[Iterable[int]] = None,
        updateStrings: Optional[bool] = None,
        cleanupMode: Optional[bool] = None,
        importOptions: Optional[UploadStringsImportOptions] = None,
        updateOption: Optional[StringUpdateOption] = None,
    ):
        """
        Upload Strings.

        String-based projects only.

        :param updateOption: Must be used together with `updateStrings = True`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#operation/api.projects.strings.uploads.post
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#operation/api.projects.strings.uploads.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_strings_uploads_path(projectId=projectId),
            request_data={
                "storageId": storageId,
                "branchId": branchId,
                "type": type,
                "parserVersion": parserVersion,
                "labelIds": labelIds,
                "updateStrings": updateStrings,
                "cleanupMode": cleanupMode,
                "importOptions": importOptions,
                "updateOption": updateOption,
            },
        )

    def upload_strings_status(self, uploadId: str, projectId: Optional[int] = None):
        """
        Upload Strings Status.

        String-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#operation/api.projects.strings.uploads.get
        https://support.crowdin.com/developer/enterprise/api/v2/string-based/#operation/api.projects.strings.uploads.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_strings_uploads_path(projectId=projectId, uploadId=uploadId),
        )


class EnterpriseSourceStringsResource(SourceStringsResource):
    """
    Resource for Source Strings (Crowdin Enterprise).

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Source-Strings
    """

    def get_reviewed_builds_path(self, projectId: int, buildId: Optional[int] = None):
        if buildId is not None:
            return f"projects/{projectId}/strings/reviewed-builds/{buildId}"

        return f"projects/{projectId}/strings/reviewed-builds"

    def list_reviewed_source_files_builds(
        self,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Reviewed Source Files Builds.

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.strings.reviewed-builds.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"branchId": branchId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_reviewed_builds_path(projectId=projectId),
            params=params,
        )

    def build_reviewed_source_files(
        self,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
    ):
        """
        Build Reviewed Source Files.

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.strings.reviewed-builds.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_reviewed_builds_path(projectId=projectId),
            request_data={"branchId": branchId},
        )

    def check_reviewed_source_files_build_status(
        self,
        buildId: int,
        projectId: Optional[int] = None,
    ):
        """
        Check Reviewed Source Files Build Status.

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.strings.reviewed-builds.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_reviewed_builds_path(projectId=projectId, buildId=buildId),
        )

    def download_reviewed_source_files(
        self,
        buildId: int,
        projectId: Optional[int] = None,
    ):
        """
        Download Reviewed Source Files.

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.strings.reviewed-builds.download.download
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_reviewed_builds_path(projectId=projectId, buildId=buildId) + "/download",
        )
