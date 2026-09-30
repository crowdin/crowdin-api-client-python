from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class ClientsResource(BaseResource):
    """
    Resource for Clients.

    Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Clients
    """

    def get_clients_path(self):
        return "clients"

    def list_clients(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        """
        List Clients

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.clients.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_clients_path(),
            params=self.get_page_params(offset=offset, limit=limit),
        )
