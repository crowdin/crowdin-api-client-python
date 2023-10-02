from unittest import mock

import pytest

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.webhooks.enums import (
    WebhookRequestType,
    WebhookContentType
)
from crowdin_api.api_resources.webhooks.organization.enums import (
    OrganizationWebhookEvent,
    OrganizationWebhookPatchPath,
    EnterpriseOrgWebhookEvent
)
from crowdin_api.api_resources.webhooks.organization.resource import OrganizationWebhooksResource
from crowdin_api.requester import APIRequester


class TestOrganizationWebhooksResource:
    resource_class = OrganizationWebhooksResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_webhooks(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_webhooks() == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(),
            path=resource.BASE_URL
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [
                        OrganizationWebhookEvent.PROJECT_CREATED,
                        OrganizationWebhookEvent.PROJECT_DELETED
                    ],
                    "request_type": WebhookRequestType.POST
                },
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [
                        OrganizationWebhookEvent.PROJECT_CREATED,
                        OrganizationWebhookEvent.PROJECT_DELETED
                    ],
                    "requestType": WebhookRequestType.POST,
                    "isActive": None,
                    "batchingEnabled": None,
                    "contentType": None,
                    "headers": None,
                    "payload": None
                }
            ),
            (
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [
                        OrganizationWebhookEvent.PROJECT_CREATED,
                        OrganizationWebhookEvent.PROJECT_DELETED
                    ],
                    "request_type": WebhookRequestType.POST,
                    "is_active": True,
                    "batching_enabled": False,
                    "content_type": WebhookContentType.APPLICATION_JSON,
                    "headers": {},
                    "payload": {}
                },
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [
                        OrganizationWebhookEvent.PROJECT_CREATED,
                        OrganizationWebhookEvent.PROJECT_DELETED
                    ],
                    "requestType": WebhookRequestType.POST,
                    "isActive": True,
                    "batchingEnabled": False,
                    "contentType": WebhookContentType.APPLICATION_JSON,
                    "headers": {},
                    "payload": {}
                }
            )
        )
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_webhook(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_webhook(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.BASE_URL,
            request_data=request_data
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
                (
                        {
                            "name": "Some",
                            "url": "https://example.com",
                            "events": [
                                EnterpriseOrgWebhookEvent.PROJECT_CREATED,
                                EnterpriseOrgWebhookEvent.PROJECT_DELETED
                            ],
                            "request_type": WebhookRequestType.POST
                        },
                        {
                            "name": "Some",
                            "url": "https://example.com",
                            "events": [
                                EnterpriseOrgWebhookEvent.PROJECT_CREATED,
                                EnterpriseOrgWebhookEvent.PROJECT_DELETED
                            ],
                            "requestType": WebhookRequestType.POST,
                            "isActive": None,
                            "batchingEnabled": None,
                            "contentType": None,
                            "headers": None,
                            "payload": None
                        }
                ),
                (
                        {
                            "name": "Some",
                            "url": "https://example.com",
                            "events": [
                                EnterpriseOrgWebhookEvent.GROUP_CREATED,
                                EnterpriseOrgWebhookEvent.GROUP_DELETED
                            ],
                            "request_type": WebhookRequestType.POST,
                            "is_active": True,
                            "batching_enabled": False,
                            "content_type": WebhookContentType.APPLICATION_JSON,
                            "headers": {},
                            "payload": {}
                        },
                        {
                            "name": "Some",
                            "url": "https://example.com",
                            "events": [
                                EnterpriseOrgWebhookEvent.GROUP_CREATED,
                                EnterpriseOrgWebhookEvent.GROUP_DELETED
                            ],
                            "requestType": WebhookRequestType.POST,
                            "isActive": True,
                            "batchingEnabled": False,
                            "contentType": WebhookContentType.APPLICATION_JSON,
                            "headers": {},
                            "payload": {}
                        }
                )
        )
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_webhook_enterprise(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_webhook(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.BASE_URL,
            request_data=request_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_webhook(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_webhook(organization_webhook_id=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_webhooks_path(organization_webhook_id=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_webhook(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_webhook(organization_webhook_id=1) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_webhooks_path(organization_webhook_id=1)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_webhook(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": OrganizationWebhookPatchPath.NAME
            },
            {
                "value": [
                    OrganizationWebhookEvent.PROJECT_CREATED
                ],
                "op": PatchOperation.REPLACE,
                "path": OrganizationWebhookPatchPath.EVENTS
            }
        ]

        resource = self.get_resource(base_absolut_url)

        assert resource.edit_webhook(
            organization_webhook_id=1,
            data=data
        ) == "response"

        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_webhooks_path(organization_webhook_id=1)
        )
