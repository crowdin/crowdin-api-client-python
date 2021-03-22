from typing import IO, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class StoragesResource(BaseResource):
    """
    Resource for Storages.

    Storage is a separate container for each file. You need to use Add Storage method before adding
    files to your projects via API. Files that should be uploaded into storage include files for
    localization, screenshots, Glossaries, and Translation Memories.

    Storage id is the identifier of the file uploaded to the Storage.

    Note: Storage is periodically cleared. The files that were already uploaded to your account will
    be removed from storage and will remain in your account.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Storage
    """

    def get_storages_path(self, storageId: Optional[int] = None):
        if storageId:
            return f"storages/{storageId}"

        return "storages"

    def list_storages(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """List Storages.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.storages.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_storages_path(),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_storage(self, file: IO):
        """Add Storage.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.storages.post
        """

        return self.requester.request(method="post", path=self.get_storages_path(), file=file)

    def get_storage(self, storageId: int):
        """Get Storage.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.storages.get
        """

        return self.requester.request(
            method="get", path=self.get_storages_path(storageId=storageId)
        )

    def delete_storage(self, storageId: int):
        """Delete Storage.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.storages.delete
        """

        return self.requester.request(
            method="delete", path=self.get_storages_path(storageId=storageId)
        )
