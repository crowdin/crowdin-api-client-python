from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.screenshots.enums import ScreenshotPatchPath, TagPatchPath
from crowdin_api.api_resources.screenshots.resource import ScreenshotsResource
from crowdin_api.requester import APIRequester


class TestSourceFilesResource:
    resource_class = ScreenshotsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    # Screenshots
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/screenshots"),
            ({"projectId": 1, "screenshotId": 2}, "projects/1/screenshots/2"),
        ),
    )
    def test_get_screenshots_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_screenshots_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_screenshots(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_screenshots(projectId=1, **{"offset": 0, "limit": 10}) == "response"
        m_request.assert_called_once_with(
            method="get",
            params={"offset": 0, "limit": 10},
            path=resource.get_screenshots_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "storageId": 1,
                    "name": "name",
                },
                {"storageId": 1, "name": "name", "autoTag": None},
            ),
            (
                {"storageId": 1, "name": "name", "autoTag": True},
                {"storageId": 1, "name": "name", "autoTag": True},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_screenshot(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_screenshot(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_screenshots_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_screenshot(projectId=1, screenshotId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.update_screenshot(projectId=1, screenshotId=2, storageId=3, name="test")
            == "response"
        )
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
            request_data={"storageId": 3, "name": "test"},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_screenshot(projectId=1, screenshotId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": ScreenshotPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_screenshot(projectId=1, screenshotId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
        )

    # Tags
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1, "screenshotId": 2}, "projects/1/screenshots/2/tags"),
            (
                {"projectId": 1, "screenshotId": 2, "tagId": 3},
                "projects/1/screenshots/2/tags/3",
            ),
        ),
    )
    def test_get_tags_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_tags_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tags(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_tags(projectId=1, screenshotId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            params={"offset": 0, "limit": 25},
            path=resource.get_tags_path(projectId=1, screenshotId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_replace_tags(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [{"stringId": 1, "position": {"x": 1, "y": 2, "width": 3, "height": 4}}]

        resource = self.get_resource(base_absolut_url)
        assert resource.replace_tags(projectId=1, screenshotId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_tags_path(
                projectId=1,
                screenshotId=2,
            ),
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_auto_tag(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.auto_tag(projectId=1, screenshotId=2, autoTag=False) == "response"
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_tags_path(
                projectId=1,
                screenshotId=2,
            ),
            request_data={"autoTag": False},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_tag(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [{"stringId": 1, "position": {"x": 1, "y": 2, "width": 3, "height": 4}}]

        resource = self.get_resource(base_absolut_url)
        assert resource.add_tag(projectId=1, screenshotId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tags_path(
                projectId=1,
                screenshotId=2,
            ),
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clear_tags(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.clear_tags(projectId=1, screenshotId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_tags_path(projectId=1, screenshotId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_tag(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_tag(projectId=1, screenshotId=2, tagId=3) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_tags_path(projectId=1, screenshotId=2, tagId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_tag(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_tag(projectId=1, screenshotId=2, tagId=3) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_tags_path(projectId=1, screenshotId=2, tagId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_tag(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": 1,
                "op": PatchOperation.REPLACE,
                "path": TagPatchPath.POSITION,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_tag(projectId=1, screenshotId=2, tagId=3, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_tags_path(projectId=1, screenshotId=2, tagId=3),
        )
