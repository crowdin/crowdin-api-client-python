from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.distributions.enums import ExportMode
from crowdin_api.api_resources.distributions.types import DistributionPatchRequest


class DistributionsResource(BaseResource):
    """
    Resource for Distributions.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Distributions
    """

    def get_distributions_path(self, projectId: int, hash: Optional[str] = None):
        if hash:
            return f"projects/{projectId}/distributions/{hash}"

        return f"projects/{projectId}/distributions"

    def list_distributions(
        self,
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Distributions.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_distributions_path(projectId=projectId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_distribution(
        self,
        name: str,
        projectId: Optional[int] = None,
        fileIds: Optional[Iterable[int]] = None,
        bundleIds: Optional[Iterable[int]] = None,
        exportMode: Optional[ExportMode] = ExportMode.DEFAULT,
    ):
        """
        Add Distribution.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_distributions_path(projectId=projectId),
            request_data={
                "exportMode": exportMode,
                "name": name,
                "fileIds": fileIds,
                "bundleIds": bundleIds
            },
        )

    def get_distribution(self, hash: str, projectId: Optional[int] = None):
        """
        Get Distribution.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_distributions_path(projectId=projectId, hash=hash),
        )

    def delete_distribution(self, hash: str, projectId: Optional[int] = None):
        """
        Delete Distribution.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_distributions_path(projectId=projectId, hash=hash),
        )

    def edit_distribution(
        self,
        hash: str,
        data: Iterable[DistributionPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Distribution.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_distributions_path(projectId=projectId, hash=hash),
            request_data=data,
        )

    def get_distribution_release(self, hash: str, projectId: Optional[int] = None):
        """
        Get Distribution Release.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.release.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"{self.get_distributions_path(projectId=projectId, hash=hash)}/release",
        )

    def release_distribution(self, hash: str, projectId: Optional[int] = None):
        """
        Release Distribution.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.distributions.release.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"{self.get_distributions_path(projectId=projectId, hash=hash)}/release",
        )
