from unittest import mock

import pytest

from crowdin_api.api_resources.fields.resource import FieldsResource
from crowdin_api.api_resources.fields.enums import (
    FieldEntity,
    FieldType,
    FieldPlace,
    FieldOperations,
    FieldsPatchPath,
)
from crowdin_api.requester import APIRequester


class TestFieldsResources:
    resource_class = FieldsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "fields"),
            ({"fieldId": 1}, "fields/1"),
        ),
    )
    def test_get_labels_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_fields_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "search": None,
                    "entity": None,
                    "type": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "search": "test",
                    "entity": FieldEntity.PROJECT,
                    "type": FieldType.CHECKBOX,
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "search": "test",
                    "entity": FieldEntity.PROJECT,
                    "type": FieldType.CHECKBOX,
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_fields(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_fields(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_fields_path(),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.CHECKBOX,
                    "entities": [FieldEntity.FILE],
                },
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.CHECKBOX,
                    "entities": [FieldEntity.FILE],
                    "description": None,
                    "config": None,
                },
            ),
            # List Field Config
            (
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.CHECKBOX,
                    "entities": [FieldEntity.FILE],
                    "description": "description",
                    "config": {
                        "options": [{"label": "string", "value": "string"}],
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}],
                    },
                },
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.CHECKBOX,
                    "entities": [FieldEntity.FILE],
                    "description": "description",
                    "config": {
                        "options": [{"label": "string", "value": "string"}],
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}],
                    },
                },
            ),
            # Number Field Config
            (
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.NUMBER,
                    "entities": [FieldEntity.PROJECT],
                    "description": "description",
                    "config": {
                        "min": 1,
                        "max": 10,
                        "units": "kg",
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}],
                    },
                },
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.NUMBER,
                    "entities": [FieldEntity.PROJECT],
                    "description": "description",
                    "config": {
                        "min": 1,
                        "max": 10,
                        "units": "kg",
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}],
                    },
                },
            ),
            # Other Field Config
            (
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.NUMBER,
                    "entities": [FieldEntity.PROJECT],
                    "description": "description",
                    "config": {
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}]
                    },
                },
                {
                    "name": "test",
                    "slug": "test-slug",
                    "type": FieldType.NUMBER,
                    "entities": [FieldEntity.PROJECT],
                    "description": "description",
                    "config": {
                        "locations": [{"place": FieldPlace.PROJECT_CREATE_MODAL}]
                    },
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_field(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_field(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_fields_path(),
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_field(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_field(fieldId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_fields_path(fieldId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_field(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_field(fieldId=1) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_fields_path(fieldId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_field(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": FieldOperations.REPLACE,
                "path": FieldsPatchPath.NAME,
                "value": "test",
            }
        ]
        fieldId = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_field(fieldId=fieldId, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_fields_path(fieldId=fieldId),
            request_data=data,
        )
