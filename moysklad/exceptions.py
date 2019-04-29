from requests import Request, Response


class PosTokenException(Exception):
    pass


class RequestFailedException(Exception):
    def __init__(self, request: Request, response: Response, *args) -> None:
        super().__init__(*args)
        self._request = request
        self._response = response

    def __str__(self):
        res = self.get_response()
        return f'RequestError [{res.status_code}]: {res.text}'

    def get_request(self):
        return self._request

    def get_response(self):
        return self._response


class ResponseParseException(Exception):
    pass


class EntityHasNoIdException(Exception):
    pass


class ApiResponseException(RequestFailedException):
    def __init__(self, request: Request, response: Response, errors) -> None:
        super().__init__(request, response)
        error = errors[0]
        self._code = error.get('code')
        self._error_text = error.get('error')
        self._more_info = error.get('moreInfo')
        self._errors = errors

    def __str__(self) -> str:
        return f'ApiError [{self.get_api_code()}]: {self.get_error_text()}'

    def get_api_code(self):
        return self._code

    def get_error_text(self):
        return self._error_text

    def get_more_info(self):
        return self._more_info

    def get_errors(self):
        return self._errors
