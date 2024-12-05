from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders
from crowdin_api.api_resources.source_strings.enums import ScopeFilter
from crowdin_api.api_resources.source_strings.types import (
    SourceStringsPatchRequest,
    StringBatchOperationPatchRequest,
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
    https://developer.crowdin.com/api/v2/#tag/Source-Strings
    """

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
    ):
        """
        List Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "branchId": branchId,
            "fileId": fileId,
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
        text: str,
        projectId: Optional[int] = None,
        identifier: Optional[str] = None,
        fileId: Optional[int] = None,
        context: Optional[str] = None,
        isHidden: Optional[bool] = None,
        maxLength: Optional[int] = None,
        labelIds: Optional[Iterable[int]] = None,
        branchId: Optional[int] = None
    ):
        """
        Add String.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.post
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
                "branchId": branchId
            },
        )

    def get_string(self, stringId: int, projectId: Optional[int] = None):
        """
        Get String.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
        )

    def delete_string(self, stringId: int, projectId: Optional[int] = None):
        """
        Delete String.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.delete
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
    ):
        """
        Edit String.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
            request_data=data,
        )

    def string_batch_operation(
        self,
        data: Iterable[StringBatchOperationPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        String Batch Operations.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.strings.batchPatch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_source_strings_path(projectId=projectId),
            request_data=data,
        )
