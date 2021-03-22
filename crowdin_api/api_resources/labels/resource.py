from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.labels.types import LabelsPatchRequest


class LabelsResource(BaseResource):
    """
    Resource for Labels.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Labels
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
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_labels_path(projectId=projectId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_label(self, projectId: int, title: str):
        """
        Add Label.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.post
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
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.get
        """

        return self.requester.request(
            method="get",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def delete_label(self, projectId: int, labelId: int):
        """
        Delete Label.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def edit_label(self, projectId: int, labelId: int, data: Iterable[LabelsPatchRequest]):
        """
        Edit Label.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
            request_data=data,
        )

    def assign_label_to_strings(self, projectId: int, labelId: int, stringIds: Iterable[int]):
        """
        Assign Label to Strings.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.strings.post
        """

        return self.requester.request(
            method="post",
            request_data={"stringIds": stringIds},
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )

    def unassign_label_from_strings(self, projectId: int, labelId: int, stringIds: Iterable[int]):
        """
        Unassign Label from Strings.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.labels.strings.deleteMany
        """

        return self.requester.request(
            method="delete",
            params={"stringIds": ",".join(str(stringId) for stringId in stringIds)},
            path=self.get_labels_path(projectId=projectId, labelId=labelId),
        )
