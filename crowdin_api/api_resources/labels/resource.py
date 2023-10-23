from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.labels.types import LabelsPatchRequest


class LabelsResource(BaseResource):
    """
    Resource for Labels.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Labels
    """

    def get_labels_path(self, projectId: int, labelId: Optional[int] = None):
        if labelId:
            return f"projects/{projectId}/labels/{labelId}"

        return f"projects/{projectId}/labels"

    def list_labels(
        self,
        projectId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Labels.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_labels_path(projectId=projectId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_label(self, projectId: int, title: str):
        """
        Add Label.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.post
        """

        return self.requester.request(
            method="post",
            path=self.get_labels_path(projectId=projectId),
            request_data={"title": title},
        )

    def get_label(self, projectId: int, labelId: int):
        """
        Get Label.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.get
        """

        return self.requester.request(
            method="get",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def delete_label(self, projectId: int, labelId: int):
        """
        Delete Label.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def edit_label(self, projectId: int, labelId: int, data: Iterable[LabelsPatchRequest]):
        """
        Edit Label.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
            request_data=data,
        )

    def get_screenshots_path(self, project_id: int, label_id: int):
        return f"projects/{project_id}/labels/{label_id}/screenshots"

    def assign_label_to_screenshots(self, project_id: int, label_id: int, screenshot_ids: Iterable[int]):
        """
        Assign Label to Screenshots

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.screenshots.post
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.labels.screenshots.post
        """

        return self.requester.request(
            method="post",
            path=self.get_screenshots_path(project_id, label_id),
            request_data={
                "screenshotIds": screenshot_ids
            }
        )

    def unassign_label_from_screenshots(self, project_id: int, label_id: int, screenshot_ids: Iterable[int]):
        """
        Unassign Label from Screenshots

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        """

        query = ",".join(str(screenshot_id) for screenshot_id in screenshot_ids)

        return self.requester.request(
            method="delete",
            path=f"{self.get_screenshots_path(project_id, label_id)}?screenshotIds={query}"
        )

    def assign_label_to_strings(self, projectId: int, labelId: int, stringIds: Iterable[int]):
        """
        Assign Label to Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.strings.post
        """

        return self.requester.request(
            method="post",
            request_data={"stringIds": stringIds},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )

    def unassign_label_from_strings(self, projectId: int, labelId: int, stringIds: Iterable[int]):
        """
        Unassign Label from Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.strings.deleteMany
        """

        return self.requester.request(
            method="delete",
            params={"stringIds": ",".join(str(stringId) for stringId in stringIds)},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )
