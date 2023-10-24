from abc import ABCMeta
from typing import Optional

from crowdin_api.requester import APIRequester


class BaseResource(metaclass=ABCMeta):
    def __init__(
        self, requester: APIRequester, project_id: Optional[int] = None, page_size=25
    ):
        self.requester = requester
        self.project_id = project_id
        self.page_size = page_size
        self._flag_fetch_all = None
        self._max_limit = None

    def get_project_id(self):
        if self.project_id is None:
            raise ValueError("You must set project id for client")
        return self.project_id

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

    def with_fetch_all(self, max_limit: Optional[int] = None):
        self._max_limit = max_limit
        self._flag_fetch_all = True
        return self

    def _get_entire_data(self, method: str, path: str, params: Optional[dict] = None):
        if not self._flag_fetch_all:
            return self.requester.request(
                method=method,
                path=path,
                params=params,
            )

        contents = self._fetch_all(
            method=method,
            path=path,
            params=params,
            max_amount=self._max_limit
        )
        self._flag_fetch_all = False
        self._max_limit = None
        return contents

    def _fetch_all(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        max_amount: Optional[int] = None
    ) -> list:
        limit = 500
        offset = 0
        join_data = []
        if params is None:
            params = {}

        if max_amount and max_amount < limit:
            limit = max_amount

        while True:
            params.update({"limit": limit, "offset": offset})

            content = self.requester.request(method=method, path=path, params=params)
            data = content.get("data", [])
            data and join_data.extend(data)

            if len(data) < limit or (max_amount and len(join_data) >= max_amount):
                break
            else:
                offset += limit

            if max_amount and max_amount < len(join_data) + limit:
                limit = max_amount - len(join_data)

        content["data"] = join_data
        return content
