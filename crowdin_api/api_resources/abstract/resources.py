from abc import ABCMeta, abstractmethod
from typing import Union, Optional

from crowdin_api.requester import APIRequester


class BaseResource(metaclass=ABCMeta):
    def __init__(self, requester: APIRequester):
        self.requester = requester

    @property
    @abstractmethod
    def base_path(self):
        """Base path for resource."""

    def prepare_path(self, object_id: Optional[Union[int, str]] = None):
        base_path = self.base_path.strip("/")

        if object_id is None:
            return base_path

        return "/".join([base_path, str(object_id)])
