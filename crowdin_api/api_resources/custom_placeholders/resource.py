from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.custom_placeholders.types import CustomPlaceholderPatchRequest


class CustomPlaceholdersResource(BaseResource):
    """
    Resource for Custom Placeholders.

    Custom placeholders of the organization. Assign them to a project with
    Add Project Placeholder.

    Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Custom-Placeholders
    """

    def get_custom_placeholders_path(self, customPlaceholderId: Optional[int] = None):
        if customPlaceholderId is not None:
            return f"custom-placeholders/{customPlaceholderId}"

        return "custom-placeholders"

    def list_custom_placeholders(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Custom Placeholders.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-placeholders.getMany
        """
        return self._get_entire_data(
            method="get",
            path=self.get_custom_placeholders_path(),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_custom_placeholder(
        self,
        definition: str,
        description: Optional[str] = None,
        argumentDelimiter: Optional[str] = None,
    ):
        """
        Add Custom Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-placeholders.post
        """
        return self.requester.request(
            method="post",
            path=self.get_custom_placeholders_path(),
            request_data={
                "definition": definition,
                "description": description,
                "argumentDelimiter": argumentDelimiter,
            },
        )

    def get_custom_placeholder(self, customPlaceholderId: int):
        """
        Get Custom Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-placeholders.get
        """
        return self.requester.request(
            method="get",
            path=self.get_custom_placeholders_path(customPlaceholderId=customPlaceholderId),
        )

    def edit_custom_placeholder(
        self,
        customPlaceholderId: int,
        data: Iterable[CustomPlaceholderPatchRequest],
    ):
        """
        Edit Custom Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-placeholders.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_custom_placeholders_path(customPlaceholderId=customPlaceholderId),
            request_data=data,
        )

    def delete_custom_placeholder(self, customPlaceholderId: int):
        """
        Delete Custom Placeholder.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-placeholders.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_custom_placeholders_path(customPlaceholderId=customPlaceholderId),
        )
