from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.screenshots.types import (
    AddTagRequest,
    ScreenshotPatchRequest,
    TagPatchRequest,
)


class ScreenshotsResource(BaseResource):
    """
    Resource for Screenshots.

    Screenshots provide translators with additional context for the source strings.
    Screenshot tags allow specifying which source strings are displayed on each screenshot.

    Use API to manage screenshots and their tags.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Screenshots
    """

    # Screenshots
    def get_screenshots_path(self, projectId: int, screenshotId: Optional[int] = None):
        if screenshotId is not None:
            return f"projects/{projectId}/screenshots/{screenshotId}"

        return f"projects/{projectId}/screenshots"

    def list_screenshots(
        self,
        projectId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Screenshots.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_screenshots_path(projectId=projectId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_screenshot(
        self,
        projectId: int,
        storageId: int,
        name: str,
        autoTag: Optional[bool] = None,
    ):
        """
        Add Screenshot.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.post
        """

        return self.requester.request(
            method="post",
            path=self.get_screenshots_path(projectId=projectId),
            request_data={
                "storageId": storageId,
                "name": name,
                "autoTag": autoTag,
            },
        )

    def get_screenshot(self, projectId: int, screenshotId: int):
        """
        Get Screenshot.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.get
        """

        return self.requester.request(
            method="get",
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def update_screenshot(self, projectId: int, screenshotId: int, storageId: int, name: str):
        """
        Update Screenshot.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.put
        """

        return self.requester.request(
            method="put",
            request_data={
                "storageId": storageId,
                "name": name,
            },
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def delete_screenshot(self, projectId: int, screenshotId: int):
        """
        Delete Screenshot.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def edit_screenshot(
        self, projectId: int, screenshotId: int, data: Iterable[ScreenshotPatchRequest]
    ):
        """
        Edit Screenshot.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    # Tags
    def get_tags_path(self, projectId: int, screenshotId: int, tagId: Optional[int] = None):
        if tagId is not None:
            return f"projects/{projectId}/screenshots/{screenshotId}/tags/{tagId}"

        return f"projects/{projectId}/screenshots/{screenshotId}/tags"

    def list_tags(
        self,
        projectId: int,
        screenshotId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tags.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def replace_tags(self, projectId: int, screenshotId: int, data: Iterable[AddTagRequest]):
        """
        Replace Tags.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.putMany
        """

        return self.requester.request(
            method="put",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data=data,
        )

    def auto_tag(self, projectId: int, screenshotId: int, autoTag: bool):
        """
        Auto Tag.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.putMany
        """

        return self.requester.request(
            method="put",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data={"autoTag": autoTag},
        )

    def add_tag(self, projectId: int, screenshotId: int, data: Iterable[AddTagRequest]):
        """
        Add Tag.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.post
        """

        return self.requester.request(
            method="post",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data=data,
        )

    def clear_tags(self, projectId: int, screenshotId: int):
        """
        Clear Tags.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.deleteMany
        """

        return self.requester.request(
            method="delete",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
        )

    def get_tag(self, projectId: int, screenshotId: int, tagId: int):
        """
        Get Tag.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.get
        """

        return self.requester.request(
            method="get",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )

    def delete_tag(self, projectId: int, screenshotId: int, tagId: int):
        """
        Delete Tag.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )

    def edit_tag(
        self, projectId: int, screenshotId: int, tagId: int, data: Iterable[TagPatchRequest]
    ):
        """
        Edit Tag.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )
