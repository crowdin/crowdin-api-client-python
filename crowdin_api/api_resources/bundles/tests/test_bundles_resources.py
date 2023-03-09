from unittest import mock

import pytest

from crowdin_api.api_resources import BundlesResource
from crowdin_api.api_resources.bundles.enums import BundlePatchPath
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester


class TestBundlesResource:
    resource_class = BundlesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/bundles"),
            ({"projectId": 1, "bundleId": 1}, "projects/1/bundles/1"),
        ),
    )
    def test_get_reports_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_bundles_path(**incoming_data) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_bundle(projectId=1, bundleId=1) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_bundles_path(projectId=1, bundleId=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_bundle(projectId=1, bundleId=1) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_bundles_path(projectId=1, bundleId=1)
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_bundles(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_bundles(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_bundles_path(projectId=1),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "name": "test_name",
                    "format": "crowdin-resx",
                    "sourcePatterns": ["/master/"],
                    "exportPattern": "strings-%two_letter_code%.resx",
                },
                {
                    "name": "test_name",
                    "format": "crowdin-resx",
                    "sourcePatterns": ["/master/"],
                    "exportPattern": "strings-%two_letter_code%.resx",
                    "ignorePatterns": None,
                    "labelIds": None,

                },
            ),
            (
                {
                    "name": "test_name",
                    "format": "crowdin-resx",
                    "sourcePatterns": ["/master/"],
                    "exportPattern": "strings-%two_letter_code%.resx",
                    "ignorePatterns": ["/master/environments/"],
                    "labelIds": [2],
                },
                {
                    "name": "test_name",
                    "format": "crowdin-resx",
                    "sourcePatterns": ["/master/"],
                    "exportPattern": "strings-%two_letter_code%.resx",
                    "ignorePatterns": ["/master/environments/"],
                    "labelIds": [2],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_bundle(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_bundle(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_bundles_path(projectId=1),
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "value",
        [
            1,
            "test"
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_bundle(self, m_request, base_absolut_url, value):
        m_request.return_value = "response"

        data = [
            {
                "value": value,
                "op": PatchOperation.REPLACE,
                "path": BundlePatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_bundle(projectId=1, bundleId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_bundles_path(projectId=1, bundleId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_bundle(projectId=1, bundleId=1, exportId="1") == "response"
        m_request.assert_called_once_with(
            method="get", path=f"{resource.get_bundles_exports_path(projectId=1, bundleId=1, exportId='1')}/download"
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_bundle(projectId=1, bundleId=1) == "response"
        m_request.assert_called_once_with(
            method="post", path=f"{resource.get_bundles_path(projectId=1, bundleId=1)}/exports"
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_bundle_export_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_bundle_export_status(projectId=1, bundleId=1, exportId="1") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_bundles_exports_path(projectId=1, bundleId=1, exportId="1")
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_bundle_list_files(
            self,
            m_request,
            incoming_data,
            request_params,
            base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        test_result = resource.get_bundle_list_files(projectId=1, bundleId=1, **incoming_data)
        assert test_result == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/bundles/1/files",
            params=request_params,
        )
