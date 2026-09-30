from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.screenshots.enums import ListScreenshotsOrderBy, ScreenshotPatchPath, TagPatchPath
from crowdin_api.api_resources.screenshots.resource import ScreenshotsResource
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestSourceFilesResource:
    resource_class = ScreenshotsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

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

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "search": None,
                    "orderBy": None,
                    "stringIds": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListScreenshotsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "stringIds": [1, 2, 3],
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "search": "home",
                    "limit": 10,
                    "offset": 0,
                },
                {
                    "search": "home",
                    "orderBy": Sorting(
                        [SortingRule(ListScreenshotsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "stringIds": "1,2,3",
                    "labelIds": "4,5,6",
                    "excludeLabelIds": "7,8,9",
                    "limit": 10,
                    "offset": 0,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_screenshots(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_screenshots(projectId=1, **incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_screenshots_path(projectId=1),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_screenshots_string_id(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        with pytest.warns(DeprecationWarning):
            assert resource.list_screenshots(projectId=1, stringId=5) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_screenshots_path(projectId=1),
            params={
                "search": None,
                "orderBy": None,
                "stringIds": "5",
                "labelIds": None,
                "excludeLabelIds": None,
                "offset": 0,
                "limit": 25,
            },
        )

    @pytest.mark.parametrize(
        "in_params, expected_params",
        [
            (
                {
                    "storageId": 1,
                    "name": "test_screenshot",
                    "projectId": 1,
                    "autoTag": True,
                    "fileId": 2,
                    "branchId": 3,
                    "directoryId": 4,
                    "labelIds": [5, 6],
                },
                {
                    "storageId": 1,
                    "name": "test_screenshot",
                    "autoTag": True,
                    "fileId": 2,
                    "branchId": 3,
                    "directoryId": 4,
                    "labelIds": [5, 6],
                },
            ),
        ],
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_screenshot(self, m_request, in_params, expected_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_screenshot(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_screenshots_path(projectId=1),
            request_data=expected_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_screenshot(
            projectId=1, screenshotId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.update_screenshot(
                projectId=1, screenshotId=2, storageId=3, name="test")
            == "response"
        )
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
            request_data={"storageId": 3, "name": "test", "usePreviousTags": None},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_screenshot_use_previous_tags(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.update_screenshot(
                projectId=1, screenshotId=2, storageId=3, name="test", usePreviousTags=False
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
            request_data={"storageId": 3, "name": "test", "usePreviousTags": False},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_screenshot(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_screenshot(
            projectId=1, screenshotId=2) == "response"
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
            },
            {
                "value": [1, 2],
                "op": PatchOperation.REPLACE,
                "path": ScreenshotPatchPath.LABEL_IDS,
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_screenshot(
            projectId=1, screenshotId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_screenshots_path(projectId=1, screenshotId=2),
        )

    # Tags
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1, "screenshotId": 2},
             "projects/1/screenshots/2/tags"),
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
            request_data={
                "autoTag": False,
                "fileId": None,
                "branchId": None,
                "directoryId": None,
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_auto_tag_with_scope(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.auto_tag(
                projectId=1, screenshotId=2, autoTag=True, fileId=3, branchId=4, directoryId=5
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_tags_path(projectId=1, screenshotId=2),
            request_data={"autoTag": True, "fileId": 3, "branchId": 4, "directoryId": 5},
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
