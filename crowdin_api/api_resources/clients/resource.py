from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class ClientsResource(BaseResource):
    """
    Resource for Clients.

    Link to documentation for enterprise:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Clients
    """

    def list_clients(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        """
        List Clients

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Clients/operation/api.clients.getMany
        """

        return self.requester.request(
            method="get",
            path="/clients",
            params=self.get_page_params(offset=offset, limit=limit)
        )
