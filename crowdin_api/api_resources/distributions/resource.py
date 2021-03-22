from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.distributions.types import DistributionPatchRequest


class DistributionsResource(BaseResource):
    """
    Resource for Distributions.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Distributions
    """

    def get_distributions_path(self, projectId: int, hash: Optional[str] = None):
        if hash:
            return f"projects/{projectId}/distributions/{hash}"

        return f"projects/{projectId}/distributions"

    def list_distributions(
        self,
        projectId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Distributions.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_distributions_path(projectId=projectId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_distribution(self, projectId: int, name: str, fileIds: Iterable[int]):
        """
        Add Distribution.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.post
        """

        return self.requester.request(
            method="post",
            path=self.get_distributions_path(projectId=projectId),
            request_data={"name": name, "fileIds": fileIds},
        )

    def get_distribution(self, projectId: int, hash: str):
        """
        Get Distribution.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.get
        """

        return self.requester.request(
            method="get", path=self.get_distributions_path(projectId=projectId, hash=hash)
        )

    def delete_distribution(self, projectId: int, hash: str):
        """
        Delete Distribution.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.delete
        """

        return self.requester.request(
            method="delete", path=self.get_distributions_path(projectId=projectId, hash=hash)
        )

    def edit_distribution(
        self, projectId: int, hash: str, data: Iterable[DistributionPatchRequest]
    ):
        """
        Edit Distribution.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_distributions_path(projectId=projectId, hash=hash),
            request_data=data,
        )

    def get_distribution_release(self, projectId: int, hash: str):
        """
        Get Distribution Release.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.release.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_distributions_path(projectId=projectId, hash=hash)}/release",
        )

    def release_distribution(self, projectId: int, hash: str):
        """
        Release Distribution.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.distributions.release.post
        """

        return self.requester.request(
            method="post",
            path=f"{self.get_distributions_path(projectId=projectId, hash=hash)}/release",
        )
