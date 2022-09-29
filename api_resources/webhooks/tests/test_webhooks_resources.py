from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.webhooks.enums import (
    WebhookContentType,
    WebhookEvents,
    WebhookPatchPath,
    WebhookRequestType,
)
from crowdin_api.api_resources.webhooks.resource import WebhooksResource
from crowdin_api.requester import APIRequester


class TestWebhooksResource:
    resource_class = WebhooksResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_webhooks(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_webhooks(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(),
            path=resource.get_webhooks_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [WebhookEvents.SUGGESTION_ADDED],
                    "requestType": WebhookRequestType.POST,
                },
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [WebhookEvents.SUGGESTION_ADDED],
                    "requestType": WebhookRequestType.POST,
                    "isActive": None,
                    "batchingEnabled": None,
                    "contentType": None,
                    "headers": None,
                    "payload": None,
                },
            ),
            (
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [WebhookEvents.SUGGESTION_ADDED],
                    "requestType": WebhookRequestType.POST,
                    "isActive": True,
                    "batchingEnabled": False,
                    "contentType": WebhookContentType.MULTIPART_FORM_DATA,
                    "headers": {},
                    "payload": {},
                },
                {
                    "name": "Some",
                    "url": "https://example.com",
                    "events": [WebhookEvents.SUGGESTION_ADDED],
                    "requestType": WebhookRequestType.POST,
                    "isActive": True,
                    "batchingEnabled": False,
                    "contentType": WebhookContentType.MULTIPART_FORM_DATA,
                    "headers": {},
                    "payload": {},
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_webhook(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_webhook(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_webhooks_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_webhook(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_webhook(projectId=1, webhookId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_webhooks_path(projectId=1, webhookId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_webhookk(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_webhook(projectId=1, webhookId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_webhooks_path(projectId=1, webhookId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_webhook(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": WebhookPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_webhook(projectId=1, webhookId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_webhooks_path(projectId=1, webhookId=2),
        )
