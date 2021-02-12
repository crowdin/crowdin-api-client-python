from crowdin_api.api_resources.abstract.mixins import BaseCRUDResourceMixin
from crowdin_api.api_resources.abstract.resources import BaseResource


class StorageResource(BaseCRUDResourceMixin, BaseResource):
    base_path = "storages"
