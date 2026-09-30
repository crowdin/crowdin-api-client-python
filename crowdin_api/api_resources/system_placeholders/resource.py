from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.system_placeholders.types import SystemPlaceholderPatchRequest


class SystemPlaceholdersResource(BaseResource):
    """
    Resource for Project System Placeholders.

    System placeholders are the placeholders Crowdin ships. Each project can turn them on and off.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Placeholders
    """

    def get_system_placeholders_path(self, projectId: int):
        return f"projects/{projectId}/system-placeholders"

    def list_system_placeholders(
        self,
        projectId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Project System Placeholders.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.system-placeholders.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_system_placeholders_path(projectId=projectId),
            params=self.get_page_params(limit=limit, offset=offset),
        )

    def system_placeholders_batch_operations(
        self,
        data: Iterable[SystemPlaceholderPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Batch Edit Project System Placeholders.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.system-placeholders.batchPatch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_system_placeholders_path(projectId=projectId),
            request_data=data,
        )
