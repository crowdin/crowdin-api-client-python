from unittest import mock

import pytest
from crowdin_api.api_resources.security_logs.enums import SecurityLogEvent
from crowdin_api.api_resources.security_logs.resource import (
    EnterpriseSecurityLogsResource,
    SecurityLogsResource,
)
from crowdin_api.requester import APIRequester


class TestSecurityLogsResource:
    resource_class = SecurityLogsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"userId": 1}, "/users/1/security-logs"),
            ({"userId": 1, "securityLogId": 2}, "/users/1/security-logs/2"),
        ),
    )
    def test_get_user_security_logs_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_user_security_logs_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "event": SecurityLogEvent.LOGIN,
                    "ipAddress": "127.0.0.1",
                    "offset": 0,
                    "limit": 10,
                },
                {
                    "event": SecurityLogEvent.LOGIN,
                    "ipAddress": "127.0.0.1",
                    "offset": 0,
                    "limit": 10,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                },
                {
                    "event": None,
                    "ipAddress": None,
                    "offset": 0,
                    "limit": 10,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_user_security_logs(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_user_security_logs(userId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_user_security_logs_path(userId=1),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_user_security_log(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_user_security_log(userId=1, securityLogId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_user_security_logs_path(userId=1, securityLogId=2),
        )


class TestEnterpriseSecurityLogsResource:

    resource_class = EnterpriseSecurityLogsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({}, "/security-logs"),
            ({"securityLogId": 1}, "/security-logs/1"),
        ),
    )
    def test_get_organization_security_logs_path(
        self, incoming_data, path, base_absolut_url
    ):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_security_logs_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "event": SecurityLogEvent.LOGIN,
                    "ipAddress": "127.0.0.1",
                    "userId": 1,
                    "offset": 0,
                    "limit": 10,
                },
                {
                    "event": SecurityLogEvent.LOGIN,
                    "ipAddress": "127.0.0.1",
                    "userId": 1,
                    "offset": 0,
                    "limit": 10,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                },
                {
                    "event": None,
                    "ipAddress": None,
                    "userId": None,
                    "offset": 0,
                    "limit": 10,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_organization_security_logs(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_organization_security_logs(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_organization_security_logs_path(),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_organization_security_log(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_security_log(securityLogId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_organization_security_logs_path(securityLogId=1),
        )
