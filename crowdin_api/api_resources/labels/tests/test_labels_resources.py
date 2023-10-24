from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.labels.enums import LabelsPatchPath
from crowdin_api.api_resources.labels.resource import LabelsResource
from crowdin_api.requester import APIRequester


class TestLabelsResource:
    resource_class = LabelsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/labels"),
            ({"projectId": 1, "labelId": 2}, "projects/1/labels/2"),
        ),
    )
    def test_get_labels_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_labels_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_translation_approvals(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_labels(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params={"limit": 25, "offset": 0},
            path=resource.get_labels_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_label(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_label(projectId=1, title="title") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_labels_path(projectId=1),
            request_data={"title": "title"},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_label(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_label(projectId=1, labelId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_labels_path(projectId=1, labelId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_label(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_label(projectId=1, labelId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_labels_path(projectId=1, labelId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_edit_label(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": LabelsPatchPath.TITLE,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_label(projectId=1, labelId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_labels_path(projectId=1, labelId=2),
        )

    @pytest.mark.parametrize(
        "in_params, body",
        [
            (
                [1, 2, 3],
                {
                    "screenshotIds": [1, 2, 3]
                }
            )
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_assign_label_to_screenshots(self, m_request, in_params, body, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.assign_label_to_screenshots(project_id=1, label_id=2, screenshot_ids=in_params)
        )
        m_request.assert_called_once_with(
            request_data=body,
            method="post",
            path=resource.get_screenshots_path(1, 2)
        )

    @pytest.mark.parametrize(
        "in_params, query_string",
        [
            (
                [1, 2, 3],
                "1,2,3"
            )
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_unassign_label_to_screenshots(self, m_request, in_params, query_string, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.unassign_label_from_screenshots(project_id=1, label_id=2, screenshot_ids=in_params)
        )
        m_request.assert_called_once_with(
            method="delete",
            path=f"{resource.get_screenshots_path(1, 2)}?screenshotIds={query_string}"
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_assign_label_to_strings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.assign_label_to_strings(projectId=1, labelId=2, stringIds=[1, 2]) == "response"
        )
        m_request.assert_called_once_with(
            request_data={"stringIds": [1, 2]},
            method="post",
            path=f"{resource.get_labels_path(projectId=1, labelId=2)}/strings",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_unassign_label_from_strings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.unassign_label_from_strings(projectId=1, labelId=2, stringIds=[1, 2])
            == "response"
        )
        m_request.assert_called_once_with(
            params={"stringIds": "1,2"},
            method="delete",
            path=f"{resource.get_labels_path(projectId=1, labelId=2)}/strings",
        )
