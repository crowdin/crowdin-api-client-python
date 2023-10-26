from unittest import mock
import pytest

from crowdin_api.requester import APIRequester
from crowdin_api.api_resources.notifications.resource import NotificationResource
from crowdin_api.api_resources.notifications.enums import MemberRole


class TestNotificationResource:
    resource_class = NotificationResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_send_notification_to_authenticated_user(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url=base_absolut_url)
        message = "TEST MESSAGE"

        assert (
            resource.send_notification_to_authenticated_user(message=message)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post", path="notify", request_data={"message": message}
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "userIds": [
                        1,
                        2,
                    ],
                    "message": "TEST MESSAGE",
                },
                {
                    "userIds": [
                        1,
                        2,
                    ],
                    "message": "TEST MESSAGE",
                },
            ),
            (
                {
                    "role": MemberRole.OWNER,
                    "message": "TEST MESSAGE",
                },
                {
                    "role": MemberRole.OWNER,
                    "message": "TEST MESSAGE",
                },
            ),
            (
                {
                    "role": MemberRole.MANAGER,
                    "message": "TEST MESSAGE",
                },
                {
                    "role": MemberRole.MANAGER,
                    "message": "TEST MESSAGE",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_send_notification_to_project_members(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url=base_absolut_url)
        projectId = 1

        assert resource.send_notification_to_project_members(
            projectId=projectId, request_data=in_params
        )
        m_request.assert_called_once_with(
            method="post",
            path=f"projects/{projectId}/notify",
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "userIds": [
                        1,
                        2,
                    ],
                    "message": "TEST MESSAGE",
                },
                {
                    "userIds": [
                        1,
                        2,
                    ],
                    "message": "TEST MESSAGE",
                },
            ),
            (
                {
                    "role": MemberRole.OWNER,
                    "message": "TEST MESSAGE",
                },
                {
                    "role": MemberRole.OWNER,
                    "message": "TEST MESSAGE",
                },
            ),
            (
                {
                    "role": MemberRole.MANAGER,
                    "message": "TEST MESSAGE",
                },
                {
                    "role": MemberRole.MANAGER,
                    "message": "TEST MESSAGE",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_send_notification_to_organization_members(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url=base_absolut_url)

        assert resource.send_notification_to_organization_members(request_data=in_params)
        m_request.assert_called_once_with(
            method="post",
            path="notify",
            request_data=request_data,
        )
