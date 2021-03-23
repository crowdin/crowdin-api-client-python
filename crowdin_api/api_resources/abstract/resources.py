from abc import ABCMeta
from typing import Optional

from crowdin_api.requester import APIRequester


class BaseResource(metaclass=ABCMeta):
    def __init__(self, requester: APIRequester, page_size=25):
        self.requester = requester
        self.page_size = page_size

    def _get_page_params(self, page: int):
        if page < 1:
            raise ValueError("The page number must be greater than or equal to 1.")

        return {"offset": max((page - 1) * self.page_size, 0), "limit": self.page_size}

    def get_page_params(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        if page is not None and (offset is not None or limit is not None):
            raise ValueError("You must set page or offset and limit.")

        if page:
            return self._get_page_params(page=page)
        else:
            offset = offset or 0
            if offset < 0:
                raise ValueError("The offset must be greater than or equal to 0.")

            limit = limit or self.page_size

            if limit < 1:
                raise ValueError("The limit must be greater than or equal to 1.")

        return {"offset": offset, "limit": limit}
