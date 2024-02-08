from datetime import datetime
from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.security_logs.enums import SecurityLogEvent


class SecurityLogsResource(BaseResource):
    """
    Resource for Security Logs

    Link to documentaion:
    https://developer.crowdin.com/api/v2/#tag/Security-Logs

    Link to documentation for enterprise:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Security-Logs
    """

    def get_user_security_logs_path(
        self, userId: int, securityLogId: Optional[int] = None
    ):
        if securityLogId is not None:
            return f"/users/{userId}/security-logs/{securityLogId}"
        return f"/users/{userId}/security-logs"

    def list_user_security_logs(
        self,
        userId: int,
        event: Optional[SecurityLogEvent] = None,
        createdAfter: Optional[datetime] = None,
        createdBefore: Optional[datetime] = None,
        ipAddress: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """
        List User Security Logs

        Link to documentaion:
        https://developer.crowdin.com/api/v2/#operation/api.users.security-logs.getMany
        """

        params = {
            "event": event,
            "createdAfter": createdAfter,
            "createdBefore": createdBefore,
            "ipAddress": ipAddress,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_user_security_logs_path(userId=userId),
            params=params,
        )

    def get_user_security_log(self, userId: int, securityLogId: int):
        """
        Get User Security Log

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.security-logs.get
        """

        return self.requester.request(
            method="get",
            path=self.get_user_security_logs_path(
                userId=userId, securityLogId=securityLogId
            ),
        )

    def get_organization_security_logs_path(self, securityLogId: Optional[int] = None):
        if securityLogId is not None:
            return f"/security-logs/{securityLogId}"
        return "/security-logs"

    def list_organization_security_logs(
        self,
        event: Optional[SecurityLogEvent] = None,
        createdAfter: Optional[datetime] = None,
        createdBefore: Optional[datetime] = None,
        ipAddress: Optional[str] = None,
        userId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """
        List Organization Security Logs

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.security-logs.getMany
        """

        params = {
            "event": event,
            "createdAfter": createdAfter,
            "createdBefore": createdBefore,
            "ipAddress": ipAddress,
            "userId": userId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_organization_security_logs_path(),
            params=params,
        )

    def get_organization_security_log(self, securityLogId: int):
        """
        Get Organization Security Log

        Link to documentaion:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.security-logs.get
        """

        return self.requester.request(
            method="get",
            path=self.get_organization_security_logs_path(securityLogId=securityLogId),
        )
