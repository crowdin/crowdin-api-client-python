import json
import logging
import mimetypes
import os
import time
from copy import copy
from typing import IO, Optional, Union
from urllib.parse import urljoin

import requests
from crowdin_api import status
from crowdin_api.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotFound,
    ParsingError,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from crowdin_api.parser import dumps, loads

logger = logging.getLogger("crowdin")


class APIRequester:
    """HTTP wrapper."""

    exception_map = {
        status.HTTP_400_BAD_REQUEST: ValidationError,
        status.HTTP_401_UNAUTHORIZED: AuthenticationFailed,
        status.HTTP_403_FORBIDDEN: PermissionDenied,
        status.HTTP_404_NOT_FOUND: NotFound,
        status.HTTP_405_METHOD_NOT_ALLOWED: MethodNotAllowed,
        status.HTTP_429_TOO_MANY_REQUESTS: Throttled,
    }

    default_exception = APIException
    default_file_content_type = "application/octet-stream"
    default_headers = {"Content-Type": "application/json"}

    def __init__(
        self,
        base_url: str,
        timeout: int = 80,
        retry_delay: Union[int, float] = 0.1,  # 100 ms
        max_retries: int = 5,
        default_headers: Optional[dict] = None,
    ):
        self.base_url = base_url
        self._session = requests.Session()
        self._retry_delay = retry_delay
        self._max_retries = max_retries

        headers = copy(self.default_headers)
        headers.update(default_headers or {})
        self.session.headers.update(headers)
        self._timeout = timeout

    @property
    def session(self) -> requests.Session:
        return self._session

    def _prepare_file(self, file, headers):
        if not file:
            return file, headers

        headers = copy(headers or {})
        headers["Content-Type"] = (
            mimetypes.MimeTypes().guess_type(file.name)[0]
            or self.default_file_content_type
        )
        headers["Crowdin-API-FileName"] = os.path.basename(file.name)
        return {"file": file}, headers

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        post_data: Optional[dict] = None,
        file: IO = None,
    ):
        files, headers = self._prepare_file(file=file, headers=headers)

        post_data = post_data or {}

        result = self.session.request(
            method,
            urljoin(self.base_url, path),
            params=loads(dumps(params or {})),
            headers=headers,
            data=dumps(
                {key: value for key, value in post_data.items() if value is not None}
            ),
            timeout=self._timeout,
            files=files,
        )

        status_code = result.status_code
        content = result.content
        headers = result.headers

        try:
            content = loads(content)
        except json.decoder.JSONDecodeError:
            raise ParsingError(
                context=content, http_status=status_code, headers=headers
            )

        # Success
        if 200 <= status_code <= 299:
            return content

        raise self.exception_map.get(status_code, self.default_exception)(
            http_status=status_code, context=content, headers=headers
        )

    def request(
        self,
        method,
        path,
        params=None,
        headers=None,
        post_data=None,
        file: IO = None,
    ):
        num_retries = 0

        while True:
            try:
                return self._request(
                    method=method,
                    path=path,
                    params=params,
                    headers=headers,
                    post_data=post_data,
                    file=file,
                )
            except APIException as err:
                num_retries += 1

                if not err.should_retry or num_retries >= self._max_retries:
                    raise err

                logger.info(
                    "Initiating retry {num_retries} for request {method} {path} "
                    "after sleeping {retry_delay} seconds.".format(
                        retry_delay=self._retry_delay,
                        num_retries=num_retries,
                        method=method,
                        path=path,
                    )
                )
                time.sleep(self._retry_delay)

    def close(self):
        self.session.close()

    def __del__(self):
        self.close()
