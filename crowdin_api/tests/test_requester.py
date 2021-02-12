from unittest import mock
from unittest.mock import Mock, PropertyMock
from urllib.parse import urljoin

import pytest

from crowdin_api import status
from crowdin_api.exceptions import APIException, ParsingError, ValidationError
from crowdin_api.requester import APIRequester


class TestAPIRequester:
    @mock.patch("crowdin_api.requester.APIRequester.session", new_callable=PropertyMock)
    def test_init_custom_params(self, m_session, base_absolut_url):
        session = Mock()
        m_session.return_value = session

        default_headers = {"some_custom_header": "value"}
        timeout = 100
        retry_delay = 1  # 1s
        max_retries = 5

        requester = APIRequester(
            base_url=base_absolut_url,
            timeout=timeout,
            retry_delay=retry_delay,  # 1s
            max_retries=max_retries,
            default_headers=default_headers,
        )

        session.headers.update.assert_called_once_with(default_headers)
        assert requester.base_url == base_absolut_url
        assert requester._timeout == timeout
        assert requester._retry_delay == retry_delay
        assert requester._max_retries == max_retries

    @mock.patch("crowdin_api.requester.APIRequester.session", new_callable=PropertyMock)
    def test_init_default_params(self, m_session, base_absolut_url):
        session = Mock()
        m_session.return_value = session

        requester = APIRequester(base_url=base_absolut_url)

        session.headers.update.assert_not_called()
        assert requester.base_url == base_absolut_url

    def test_session_property(self, base_absolut_url):
        requester = APIRequester(base_url=base_absolut_url)

        assert requester.session == requester._session

        with pytest.raises(AttributeError):
            requester.session = None

    @pytest.mark.parametrize(
        "should_retry,max_retries,retry_delay,num_retries",
        (
            (True, 2, 1, 2),
            (True, 3, 2, 3),
            (False, 2, 1, 1),
            (False, 10, 1, 1),
        ),
    )
    @mock.patch("time.sleep", return_value=None)
    @mock.patch("crowdin_api.requester.APIRequester._request")
    def test_request(
        self,
        m_request,
        m_sleep,
        base_absolut_url,
        should_retry,
        max_retries,
        retry_delay,
        num_retries,
    ):
        class SomeException(APIException):
            def __init__(self, headers=None, detail=None):
                super().__init__(
                    detail=detail, headers=headers, http_status=None, should_retry=should_retry
                )

        m_request.side_effect = SomeException

        requester = APIRequester(
            base_url=base_absolut_url, max_retries=max_retries, retry_delay=retry_delay, timeout=0
        )

        kw = {
            "method": "get",
            "path": "test",
            "params": {"test": "value"},
            "post_data": {"should_retry": should_retry},
        }

        with pytest.raises(APIException):
            requester.request(**kw)

        assert m_request.call_count == num_retries
        assert m_sleep.call_count == num_retries - 1

    @pytest.mark.parametrize(
        "status_code,exception",
        (
            (status.HTTP_500_INTERNAL_SERVER_ERROR, APIException),
            (status.HTTP_400_BAD_REQUEST, ValidationError),
        ),
    )
    def test__request_with_not_success_status(
        self, status_code, exception, requests_mock, base_absolut_url
    ):
        path = "test"
        requester = APIRequester(base_url=base_absolut_url)
        requests_mock.get(urljoin(base_absolut_url, path), status_code=status_code, text="{}")

        with pytest.raises(exception):
            requester._request(method="get", path=path)

    def test__request_wrong_response(self, requests_mock, base_absolut_url):
        path = "test"
        requester = APIRequester(base_url=base_absolut_url)
        requests_mock.get(urljoin(base_absolut_url, path), text="{ is not JSON ]")

        with pytest.raises(ParsingError):
            requester._request(method="get", path=path)

    @pytest.mark.parametrize("status_code", (200, 299))
    def test__request_with_success_status(self, status_code, requests_mock, base_absolut_url):
        path = "test"
        requester = APIRequester(base_url=base_absolut_url)
        requests_mock.get(
            urljoin(base_absolut_url, path), status_code=status_code, text='{"test": 1}'
        )

        assert requester._request(method="get", path=path) == {"test": 1}

    @mock.patch("crowdin_api.requester.APIRequester.session", new_callable=PropertyMock)
    def test_close(self, m_session, base_absolut_url):
        session = Mock()
        m_session.return_value = session

        requester = APIRequester(base_url=base_absolut_url)
        requester.close()
        session.close.assert_called_once()

    @mock.patch("crowdin_api.requester.APIRequester.close")
    def test_destructor(self, m_close, base_absolut_url):
        m_close.return_value = Mock()

        _requester = APIRequester(base_url=base_absolut_url)

        m_close.assert_not_called()

        _requester = None
        m_close.assert_called_once()
