from typing import Iterable, Optional

import warnings
from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.screenshots.types import (
    AddTagRequest,
    ScreenshotPatchRequest,
    TagPatchRequest,
)
from crowdin_api.sorting import Sorting


class ScreenshotsResource(BaseResource):
    """
    Resource for Screenshots.

    Screenshots provide translators with additional context for the source strings.
    Screenshot tags allow specifying which source strings are displayed on each screenshot.

    Use API to manage screenshots and their tags.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Screenshots
    """

    # Screenshots
    def get_screenshots_path(self, projectId: int, screenshotId: Optional[int] = None):
        if screenshotId is not None:
            return f"projects/{projectId}/screenshots/{screenshotId}"

        return f"projects/{projectId}/screenshots"

    def list_screenshots(
        self,
        orderBy: Optional[Sorting] = None,
        projectId: Optional[int] = None,
        stringId: Optional[int] = None,
        stringIds: Optional[Iterable[int]] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Screenshots.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.getMany
        """

        projectId = projectId or self.get_project_id()

        if stringId:
            warnings.warn("`stringId` is deprecated, use `stringIds` instead", category=DeprecationWarning)
            stringIds = [stringId]

        params = {"orderBy": orderBy, "stringIds": stringIds, "labelIds": labelIds, "excludeLabelIds": excludeLabelIds}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_screenshots_path(projectId=projectId),
            params=params,
        )

    def add_screenshot(
        self,
        storageId: int,
        name: str,
        projectId: Optional[int] = None,
        autoTag: Optional[bool] = None,
        fileId: Optional[int] = None,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        labelIds: Optional[Iterable[int]] = None,
    ):
        """
        Add Screenshot.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_screenshots_path(projectId=projectId),
            request_data={
                "storageId": storageId,
                "name": name,
                "autoTag": autoTag,
                "fileId": fileId,
                "branchId": branchId,
                "directoryId": directoryId,
                "labelIds": labelIds,
            },
        )

    def get_screenshot(self, screenshotId: int, projectId: Optional[int] = None):
        """
        Get Screenshot.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def update_screenshot(
        self,
        screenshotId: int,
        storageId: int,
        name: str,
        projectId: Optional[int] = None,
    ):
        """
        Update Screenshot.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            request_data={
                "storageId": storageId,
                "name": name,
            },
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def delete_screenshot(self, screenshotId: int, projectId: Optional[int] = None):
        """
        Delete Screenshot.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_screenshots_path(projectId=projectId, screenshotId=screenshotId),
        )

    def edit_screenshot(
        self,
        screenshotId: int,
        data: Iterable[ScreenshotPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Screenshot.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.patch
        """

        projectId = projectId or self.get_project_id()

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
        screenshotId: int,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tags.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def replace_tags(
        self,
        screenshotId: int,
        data: Iterable[AddTagRequest],
        projectId: Optional[int] = None,
    ):
        """
        Replace Tags.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.putMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data=data,
        )

    def auto_tag(
        self, screenshotId: int, autoTag: bool, projectId: Optional[int] = None
    ):
        """
        Auto Tag.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.putMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data={"autoTag": autoTag},
        )

    def add_tag(
        self,
        screenshotId: int,
        data: Iterable[AddTagRequest],
        projectId: Optional[int] = None,
    ):
        """
        Add Tag.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
            request_data=data,
        )

    def clear_tags(self, screenshotId: int, projectId: Optional[int] = None):
        """
        Clear Tags.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.deleteMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId),
        )

    def get_tag(self, screenshotId: int, tagId: int, projectId: Optional[int] = None):
        """
        Get Tag.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )

    def delete_tag(
        self, screenshotId: int, tagId: int, projectId: Optional[int] = None
    ):
        """
        Delete Tag.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )

    def edit_tag(
        self,
        screenshotId: int,
        tagId: int,
        data: Iterable[TagPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Tag.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.screenshots.tags.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_tags_path(projectId=projectId, screenshotId=screenshotId, tagId=tagId),
        )
