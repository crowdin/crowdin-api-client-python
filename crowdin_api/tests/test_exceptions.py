from unittest import mock
from unittest.mock import Mock, PropertyMock

import pytest
from crowdin_api import status
from crowdin_api.exceptions import APIException, CrowdinException


class TestCrowdinException:
    def test_init(self):
        detail = "some detail"
        exception = CrowdinException(detail=detail)
        assert exception._detail == detail

    def test_message(self):
        detail = "some detail"
        exception = CrowdinException(detail=detail)
        assert exception.message == detail

    def test_str(self):
        detail = "some detail"
        exception = CrowdinException(detail=detail)
        assert str(exception) == "CrowdinException: some detail"
        assert exception.__repr__() == "CrowdinException: some detail"


class TestAPIException:
    @pytest.mark.parametrize(
        "status_code,should_retry,result",
        (
            (status.HTTP_500_INTERNAL_SERVER_ERROR, None, True),
            (status.HTTP_500_INTERNAL_SERVER_ERROR, False, False),
            (status.HTTP_400_BAD_REQUEST, None, False),
            (status.HTTP_400_BAD_REQUEST, True, True),
            (status.HTTP_100_CONTINUE, None, False),
            (status.HTTP_100_CONTINUE, True, True),
            (status.HTTP_301_MOVED_PERMANENTLY, None, False),
            (status.HTTP_301_MOVED_PERMANENTLY, True, True),
        ),
    )
    def test_init(self, status_code, should_retry, result):
        context = "some detail"
        exception = APIException(
            context=context, http_status=status_code, should_retry=should_retry
        )
        assert exception.should_retry == result

    @pytest.mark.parametrize(
        "headers,result",
        (
            ({"request-id": 1}, 1),
            ({"request-ids": 1}, None),
        ),
    )
    def test_request_id(self, headers, result):
        exception = APIException(headers=headers)
        assert exception.request_id == result

    @mock.patch("crowdin_api.exceptions.APIException.template", new_callable=PropertyMock)
    def test_message(self, m_template):
        m_template.return_value = "template"

        exc = APIException(http_status=1, headers={"request-id": 2}, context=3)

        assert exc.message == "template"

        template = Mock()
        m_template.return_value = template
        exc = APIException()
        _ = exc.message

        template.format.assert_called_once_with(exc=exc)
