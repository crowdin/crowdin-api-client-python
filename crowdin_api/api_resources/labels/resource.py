from typing import Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.labels.types import LabelsPatchRequest
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_to_query_list


class LabelsResource(BaseResource):
    """
    Resource for Labels.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Labels

    Link to documentation for enterprise:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Labels
    """

    def get_labels_path(self, projectId: int, labelId: Optional[int] = None):
        if labelId:
            return f"projects/{projectId}/labels/{labelId}"

        return f"projects/{projectId}/labels"

    def list_labels(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        isSystem: Optional[Union[bool, int]] = None,
    ):
        """
        List Labels.

        `isSystem` (filter by system labels) is for string-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.getMany
        https://support.crowdin.com/developer/api/v2/string-based/#operation/api.projects.labels.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "isSystem": None if isSystem is None else int(isSystem),
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_labels_path(projectId=projectId),
            params=params,
        )

    def add_label(self, title: str, projectId: Optional[int] = None):
        """
        Add Label.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_labels_path(projectId=projectId),
            request_data={"title": title},
        )

    def get_label(self, labelId: int, projectId: Optional[int] = None):
        """
        Get Label.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def delete_label(self, labelId: int, projectId: Optional[int] = None):
        """
        Delete Label.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def edit_label(
        self,
        labelId: int,
        data: Iterable[LabelsPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Label.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
            request_data=data,
        )

    def get_screenshots_path(self, project_id: int, label_id: int):
        return f"projects/{project_id}/labels/{label_id}/screenshots"

    def assign_label_to_screenshots(
        self,
        label_id: int,
        screenshot_ids: Union[int, Iterable[int]],
        project_id: Optional[int] = None,
    ):
        """
        Assign Label to Screenshots

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.screenshots.post
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.labels.screenshots.post
        """

        project_id = project_id or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_screenshots_path(project_id, label_id),
            request_data={
                "screenshotIds": [screenshot_ids] if isinstance(screenshot_ids, int) else screenshot_ids
            }
        )

    def unassign_label_from_screenshots(
        self,
        label_id: int,
        screenshot_ids: Union[int, Iterable[int]],
        project_id: Optional[int] = None,
    ):
        """
        Unassign Label from Screenshots

        `screenshot_ids` can be a single screenshot identifier or an iterable of them
        (up to 500 at a time).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        """

        project_id = project_id or self.get_project_id()

        return self.requester.request(
            method="delete",
            params={"screenshotIds": convert_to_query_list(screenshot_ids)},
            path=self.get_screenshots_path(project_id, label_id),
        )

    def assign_label_to_strings(
        self,
        labelId: int,
        stringIds: Union[int, Iterable[int]],
        projectId: Optional[int] = None,
    ):
        """
        Assign Label to Strings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.strings.post
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.labels.strings.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            request_data={"stringIds": [stringIds] if isinstance(stringIds, int) else stringIds},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )

    def unassign_label_from_strings(
        self,
        labelId: int,
        stringIds: Union[int, Iterable[int]],
        projectId: Optional[int] = None,
    ):
        """
        Unassign Label from Strings.

        `stringIds` can be a single string identifier or an iterable of them
        (up to 500 at a time).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.labels.strings.deleteMany
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.labels.strings.deleteMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            params={"stringIds": convert_to_query_list(stringIds)},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )
