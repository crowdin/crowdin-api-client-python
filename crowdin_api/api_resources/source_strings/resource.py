from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders
from crowdin_api.api_resources.source_strings.enums import ScopeFilter
from crowdin_api.api_resources.source_strings.types import SourceStringsPatchRequest


class SourceStringsResource(BaseResource):
    """
    Resource for Source Strings.

    Source strings are the text units for translation. Instead of modifying source files,
    you can manage source strings one by one.

    Use API to add, edit, or delete some specific strings in the source-based and files-based
    projects (available only for the following file formats: CSV, RESX, JSON, Android XML,
    iOS strings, PROPERTIES, XLIFF).

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Source-Strings
    """

    def get_source_strings_path(self, projectId: int, stringId: Optional[int] = None):
        if stringId is not None:
            return f"projects/{projectId}/strings/{stringId}"

        return f"projects/{projectId}/strings"

    def list_strings(
        self,
        projectId: int,
        fileId: Optional[int] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        labelIds: Optional[Iterable[int]] = None,
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
        https://support.crowdin.com/api/v2/#operation/api.projects.strings.getMany
        """

        params = {
            "fileId": fileId,
            "denormalizePlaceholders": denormalizePlaceholders,
            "labelIds": None if labelIds is None else ",".join(str(item) for item in labelIds),
            "filter": filter,
            "croql": croql,
            "scope": scope,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_source_strings_path(projectId=projectId),
            params=params,
        )

    def add_string(
        self,
        projectId: int,
        text: str,
        identifier: Optional[str] = None,
        fileId: Optional[int] = None,
        context: Optional[str] = None,
        isHidden: Optional[bool] = None,
        maxLength: Optional[int] = None,
    ):
        """
        Add String.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.strings.post
        """

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
            },
        )

    def get_string(self, projectId: int, stringId: int):
        """
        Get String.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.strings.get
        """

        return self.requester.request(
            method="get",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
        )

    def delete_string(self, projectId: int, stringId: int):
        """
        Delete String.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.strings.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
        )

    def edit_string(self, projectId: int, stringId: int, data: Iterable[SourceStringsPatchRequest]):
        """
        Edit String.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.strings.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_source_strings_path(projectId=projectId, stringId=stringId),
            request_data=data,
        )
