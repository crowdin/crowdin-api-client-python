from crowdin_api import status


class CrowdinException(Exception):
    def __init__(self, detail=None):
        super().__init__(detail)
        self._detail = detail

    @property
    def message(self):
        return self._detail

    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.message)

    def __repr__(self):
        return self.__str__()


class APIException(CrowdinException):
    template = "http_status={0}, request_id={1}, detail={2}"
    default_http_status = None

    def __init__(self, detail=None, http_status=None, headers=None, should_retry=None):
        super().__init__(detail=detail)
        self.headers = headers or {}
        self.http_status = http_status or self.default_http_status

        if should_retry is None:
            if http_status is None or 100 <= http_status <= 199 or 300 <= http_status <= 499:
                should_retry = False
            else:
                should_retry = True

        self.should_retry = should_retry

    @property
    def request_id(self):
        return self.headers.get("request-id", None)

    @property
    def message(self):
        return self.template.format(self.http_status, self.request_id, self._detail)


class ParsingError(APIException):
    template = "http_status={0}, request_id={1}, detail=Error while parsing <{2}>"


class AuthenticationFailed(APIException):
    default_http_status = status.HTTP_401_UNAUTHORIZED
    template = "http_status={0}, request_id={1}, detail=Incorrect authentication credentials"


class PermissionDenied(APIException):
    default_http_status = status.HTTP_403_FORBIDDEN
    template = (
        "http_status={0}, request_id={1}, detail=You do not have permission to perform this action"
    )


class NotFound(APIException):
    default_http_status = status.HTTP_404_NOT_FOUND
    template = "http_status={0}, request_id={1}, detail=Not found."


class MethodNotAllowed(APIException):
    default_http_status = status.HTTP_405_METHOD_NOT_ALLOWED
    template = "http_status={0}, request_id={1}, detail=Method not allowed."


class Throttled(APIException):
    default_http_status = status.HTTP_429_TOO_MANY_REQUESTS
    template = "http_status={0}, request_id={1}, detail=Request was throttled."


class ValidationError(APIException):
    default_http_status = status.HTTP_400_BAD_REQUEST
    template = "http_status={0}, request_id={1}, detail=Invalid input."
