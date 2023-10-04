
from typing import Optional, Iterable, Dict

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.webhooks.enums import WebhookRequestType, WebhookContentType
from crowdin_api.api_resources.webhooks.organization.enums import OrganizationWebhookEvent, EnterpriseOrgWebhookEvent
from crowdin_api.api_resources.webhooks.organization.types import OrganizationWebhookPatchRequest


class OrganizationWebhooksResource(BaseResource):
    BASE_URL = "/webhooks"

    def get_webhooks_path(
        self,
        organization_webhook_id: int
    ):
        return f"{self.BASE_URL}/{organization_webhook_id}"

    """Webhooks allow you to collect information about events that happen in your Crowdin account. You can select the
    request type, content type, and add a custom payload, which allows you to create integrations with other systems
    on your own.

    You can configure webhooks for the following events:

    - project is created
    - project is deleted

    Use API to create, modify, and delete specific webhooks.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Organization-Webhooks
    """

    def list_webhooks(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List Webhooks

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.webhooks.getMany
        """
        return self._get_entire_data(
            method="get",
            path=self.BASE_URL,
            params=self.get_page_params(
                page=page,
                offset=offset,
                limit=limit
            )
        )

    def add_webhook(
        self,
        name: str,
        url: str,
        events: Iterable[OrganizationWebhookEvent],
        request_type: WebhookRequestType,
        is_active: Optional[bool] = None,
        batching_enabled: Optional[bool] = None,
        content_type: Optional[WebhookContentType] = None,
        headers: Optional[Dict] = None,
        payload: Optional[Dict] = None
    ):
        """
        Add webhook
        For Enterprise please use method "add_webhook_enterprise"

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.webhooks.post
        """

        return self.requester.request(
            method="post",
            path=self.BASE_URL,
            request_data={
                "name": name,
                "url": url,
                "events": events,
                "requestType": request_type,
                "isActive": is_active,
                "batchingEnabled": batching_enabled,
                "contentType": content_type,
                "headers": headers,
                "payload": payload
            }
        )

    def add_webhook_enterprise(
        self,
        name: str,
        url: str,
        events: Iterable[EnterpriseOrgWebhookEvent],
        request_type: WebhookRequestType,
        is_active: Optional[bool] = None,
        batching_enabled: Optional[bool] = None,
        content_type: Optional[WebhookContentType] = None,
        headers: Optional[Dict] = None,
        payload: Optional[Dict] = None
    ):
        """
        Add webhook (enterprise)
        Events list is different

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.webhooks.post
        """

        return self.requester.request(
            method="post",
            path=self.BASE_URL,
            request_data={
                "name": name,
                "url": url,
                "events": events,
                "requestType": request_type,
                "isActive": is_active,
                "batchingEnabled": batching_enabled,
                "contentType": content_type,
                "headers": headers,
                "payload": payload
            }
        )

    def get_webhook(
        self,
        organization_webhook_id: int
    ):
        """
        Get webhook

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.webhooks.get
        """
        return self.requester.request(
            method="get",
            path=self.get_webhooks_path(organization_webhook_id)
        )

    def delete_webhook(
        self,
        organization_webhook_id: int
    ):
        """
        Delete webhook

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.webhooks.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_webhooks_path(organization_webhook_id)
        )

    def edit_webhook(
        self,
        organization_webhook_id: int,
        data: Iterable[OrganizationWebhookPatchRequest]
    ):
        """
        Edit webhook

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.webhooks.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_webhooks_path(organization_webhook_id),
            request_data=data
        )
