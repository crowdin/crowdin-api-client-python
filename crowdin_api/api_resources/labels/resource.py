from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.labels.types import LabelsPatchRequest
from crowdin_api.sorting import Sorting


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
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Labels.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"orderBy": orderBy}
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.get
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.delete
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.patch
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
        screenshot_ids: Iterable[int],
        project_id: Optional[int] = None,
    ):
        """
        Assign Label to Screenshots

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.screenshots.post
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.labels.screenshots.post
        """

        project_id = project_id or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_screenshots_path(project_id, label_id),
            request_data={
                "screenshotIds": screenshot_ids
            }
        )

    def unassign_label_from_screenshots(
        self,
        label_id: int,
        screenshot_ids: Iterable[int],
        project_id: Optional[int] = None,
    ):
        """
        Unassign Label from Screenshots

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.labels.screenshots.deleteMany
        """

        project_id = project_id or self.get_project_id()
        query = ",".join(str(screenshot_id) for screenshot_id in screenshot_ids)

        return self.requester.request(
            method="delete",
            path=f"{self.get_screenshots_path(project_id, label_id)}?screenshotIds={query}"
        )

    def assign_label_to_strings(
        self, labelId: int, stringIds: Iterable[int], projectId: Optional[int] = None
    ):
        """
        Assign Label to Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.strings.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            request_data={"stringIds": stringIds},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )

    def unassign_label_from_strings(
        self, labelId: int, stringIds: Iterable[int], projectId: Optional[int] = None
    ):
        """
        Unassign Label from Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.labels.strings.deleteMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            params={"stringIds": ",".join(str(stringId) for stringId in stringIds)},
            path=f"{self.get_labels_path(projectId=projectId, labelId=labelId)}/strings",
        )
