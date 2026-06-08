from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.style_guides.enums import (
    ListStyleGuidesOrderBy,
    StyleGuidePatchPath,
)
from crowdin_api.api_resources.style_guides.resource import StyleGuidesResource
from crowdin_api.api_resources.style_guides.types import AddStyleGuideRequest
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestStyleGuidesResource:
    resource_class = StyleGuidesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "style-guides"),
            ({"style_guide_id": 2}, "style-guides/2"),
        ),
    )
    def test_get_style_guides_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_style_guides_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "userId": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "order_by": Sorting(
                        [SortingRule(ListStyleGuidesOrderBy.CREATED_AT, SortingOrder.DESC)]
                    ),
                    "user_id": 2,
                    "limit": 25,
                    "offset": 0,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListStyleGuidesOrderBy.CREATED_AT, SortingOrder.DESC)]
                    ),
                    "userId": 2,
                    "limit": 25,
                    "offset": 0,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_style_guides(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_style_guides(**incoming_data) == "response"

        m_request.assert_called_once_with(
            method="get",
            path="style-guides",
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                AddStyleGuideRequest(
                    name="Be My Eyes iOS's Style Guide",
                    storageId=1,
                ),
                {
                    "name": "Be My Eyes iOS's Style Guide",
                    "storageId": 1,
                },
            ),
            (
                AddStyleGuideRequest(
                    name="Be My Eyes iOS's Style Guide",
                    storageId=1,
                    aiInstructions="Rules to be used by AI models",
                    languageIds=["uk", "fr", "de"],
                    projectIds=[1, 2, 3],
                    isShared=False,
                ),
                {
                    "name": "Be My Eyes iOS's Style Guide",
                    "storageId": 1,
                    "aiInstructions": "Rules to be used by AI models",
                    "languageIds": ["uk", "fr", "de"],
                    "projectIds": [1, 2, 3],
                    "isShared": False,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_style_guide(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_style_guide(incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path="style-guides",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_style_guide(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_style_guide(style_guide_id=2) == "response"

        m_request.assert_called_once_with(
            method="get",
            path="style-guides/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_style_guide(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_style_guide(style_guide_id=2) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path="style-guides/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_style_guide(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        request_data = [
            {
                "op": PatchOperation.REPLACE,
                "path": StyleGuidePatchPath.NAME,
                "value": "Be My Eyes iOS's Style Guide",
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_style_guide(style_guide_id=2, request_data=request_data) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path="style-guides/2",
            request_data=request_data,
        )
