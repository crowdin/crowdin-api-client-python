from unittest import mock

import pytest

from crowdin_api.api_resources.enums import DenormalizePlaceholders, PluralCategoryName
from crowdin_api.api_resources.string_corrections.enums import ListCorrectionsOrderBy
from crowdin_api.api_resources.string_corrections.resource import StringCorrectionsResource
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import SortingRule, Sorting, SortingOrder


class TestStringCorrectionsResource:
    resource_class = StringCorrectionsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "string_id": 1
                },
                {
                    "stringId": 1,
                    "limit": None,
                    "offset": None,
                    "orderBy": None,
                    "denormalizePlaceholders": None
                },
            ),
            (
                {
                    "string_id": 1,
                    "limit": 25,
                    "offset": 0,
                    "order_by": Sorting(
                        [
                            SortingRule(ListCorrectionsOrderBy.CREATED_AT, SortingOrder.DESC),
                            SortingRule(ListCorrectionsOrderBy.ID)
                        ]
                    ),
                    "denormalize_placeholders": DenormalizePlaceholders.ENABLE
                },
                {
                    "stringId": 1,
                    "limit": 25,
                    "offset": 0,
                    "orderBy": "createdAt desc,id",
                    "denormalizePlaceholders": 1
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_corrections(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.list_corrections(project_id, **in_params) == "response"
        m_request.assert_called_with(
            method="get",
            path=f"projects/{project_id}/corrections",
            params=request_params
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "string_id": 1,
                    "text": "sample",
                    "plural_category_name": PluralCategoryName.ZERO
                },
                {
                    "stringId": 1,
                    "text": "sample",
                    "pluralCategoryName": "zero"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_correction(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.add_correction(project_id, **in_params) == "response"
        m_request.assert_called_with(
            method="post",
            path=f"projects/{project_id}/corrections",
            request_data=request_params
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_corrections(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        string_id = 2
        resource = self.get_resource(base_absolut_url)
        assert resource.delete_corrections(project_id, string_id) == "response"

        m_request.assert_called_with(
            method="delete",
            path=f"projects/{project_id}/corrections",
            params={
                "stringId": string_id,
            }
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "denormalize_placeholders": DenormalizePlaceholders.ENABLE,
                },
                {
                    "denormalizePlaceholders": 1
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_correction(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        correction_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.get_correction(project_id, correction_id, **in_params) == "response"
        m_request.assert_called_with(
            method="get",
            path=f"projects/{project_id}/corrections/{correction_id}",
            params=request_params
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_restore_correction(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        correction_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.restore_correction(project_id, correction_id) == "response"
        m_request.assert_called_with(
            method="put",
            path=f"projects/{project_id}/corrections/{correction_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_correction(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        project_id = 1
        correction_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_correction(project_id, correction_id) == "response"

        m_request.assert_called_with(
            method="delete",
            path=f"projects/{project_id}/corrections/{correction_id}",
        )