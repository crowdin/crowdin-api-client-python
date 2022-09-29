from crowdin_api import status


class CrowdinException(Exception):
    def __init__(self, detail=None):
        super().__init__(detail)
        self._detail = detail

    @property
    def message(self):
        return self._detail

    def __str__(self):
        return "{class_name}: {message}".format(
            class_name=self.__class__.__name__, message=self.message
        )

    def __repr__(self):
        return self.__str__()


class APIException(CrowdinException):
    default_http_status = None
    template = (
        "http_status={exc.http_status}, "
        "request_id={exc.request_id}, "
        "detail: {exc._detail}, "
        "context={exc.context}"
    )

    def __init__(
        self,
        detail=None,
        context=None,
        http_status=None,
        headers=None,
        should_retry=None,
    ):
        super().__init__(detail=detail)
        self.context = context
        self.headers = headers or {}
        self.http_status = http_status or self.default_http_status

        if should_retry is None:
            if (
                http_status is None
                or 100 <= http_status <= 199
                or 300 <= http_status <= 499
            ):
                should_retry = False
            else:
                should_retry = True

        self.should_retry = should_retry

    @property
    def request_id(self):
        return self.headers.get("request-id", None)

    @property
    def message(self):
        return self.template.format(exc=self)


class ParsingError(APIException):
    detail = "Error while parsing."


class AuthenticationFailed(APIException):
    default_http_status = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect authentication credentials"


class PermissionDenied(APIException):
    default_http_status = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to perform this action"


class NotFound(APIException):
    default_http_status = status.HTTP_404_NOT_FOUND
    detail = "Not found."


class MethodNotAllowed(APIException):
    default_http_status = status.HTTP_405_METHOD_NOT_ALLOWED
    detail = "Method not allowed."


class Throttled(APIException):
    default_http_status = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Request was throttled."


class ValidationError(APIException):
    default_http_status = status.HTTP_400_BAD_REQUEST
    detail = "Invalid input."
