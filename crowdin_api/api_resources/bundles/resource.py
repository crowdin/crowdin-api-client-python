from typing import Optional, Iterable

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.bundles.types import BundlePatchRequest


class BundlesResource(BaseResource):
    """
    Resource for Bundles.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Bundles

    Link to documentation for enterprise:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Bundles
    """
    def get_bundles_path(self, projectId: int, bundleId: Optional[int] = None):
        if bundleId:
            return f"projects/{projectId}/bundles/{bundleId}"

        return f"projects/{projectId}/bundles"

    def get_bundles_exports_path(self, projectId: int, bundleId: int, exportId: Optional[str] = None):
        bundles_path = self.get_bundles_path(projectId, bundleId)
        if exportId:
            return f"{bundles_path}/exports/{exportId}"
        return f"{bundles_path}/exports"

    def list_bundles(
        self,
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Bundles.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.getMany

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.post
        """

        params = self.get_page_params(offset=offset, limit=limit)
        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_bundles_path(projectId=projectId),
            params=params,
        )

    def add_bundle(
        self,
        name: str,
        format: str,
        sourcePatterns: Iterable[str],
        exportPattern: str,
        projectId: Optional[int] = None,
        ignorePatterns: Optional[Iterable[str]] = None,
        isMultilingual: Optional[bool] = None,
        includeProjectSourceLanguage: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
    ):
        """
        Add Bundles.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_bundles_path(projectId=projectId),
            request_data={
                "name": name,
                "format": format,
                "sourcePatterns": sourcePatterns,
                "exportPattern": exportPattern,
                "ignorePatterns": ignorePatterns,
                "isMultilingual": isMultilingual,
                "includeProjectSourceLanguage": includeProjectSourceLanguage,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
            }
        )

    def get_bundle(self, bundleId: int, projectId: Optional[int] = None):
        """
        Get Bundle.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_bundles_path(projectId=projectId, bundleId=bundleId),
        )

    def delete_bundle(self, bundleId: int, projectId: Optional[int] = None):
        """
        Delete Bundle.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.delete

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_bundles_path(projectId=projectId, bundleId=bundleId),
        )

    def edit_bundle(
        self,
        bundleId: int,
        data: Iterable[BundlePatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Bundle.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.patch

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_bundles_path(projectId=projectId, bundleId=bundleId),
            request_data=data,
        )

    def download_bundle(
        self, bundleId: int, exportId: str, projectId: Optional[int] = None
    ):
        """
        Download bundle.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.exports.download.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.exports.download.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"{self.get_bundles_exports_path(projectId=projectId, bundleId=bundleId, exportId=exportId)}/download",
        )

    def export_bundle(self, bundleId: int, projectId: Optional[int] = None):
        """
        Export bundle.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.exports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.exports.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_bundles_exports_path(projectId=projectId, bundleId=bundleId),
        )

    def check_bundle_export_status(
        self, bundleId: int, exportId: str, projectId: Optional[int] = None
    ):
        """
        Check Bundle Export Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.exports.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.exports.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_bundles_exports_path(projectId=projectId, bundleId=bundleId, exportId=exportId),
        )

    def get_bundle_list_files(
        self,
        bundleId: int,
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get Bundle List Files.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.bundles.files.getMany

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.bundles.files.getMany
        """

        params = self.get_page_params(offset=offset, limit=limit)
        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"{self.get_bundles_path(projectId=projectId, bundleId=bundleId)}/files",
            params=params,
        )
