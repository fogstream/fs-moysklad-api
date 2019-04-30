from json import JSONDecodeError

from requests import Response


class PosTokenException(Exception):
    def __str__(self) -> str:
        return 'POS token is used, but it\'s invalid or empty'


class RequestFailedException(Exception):
    def __init__(self, response: Response) -> None:
        super().__init__()
        self.request = response.request
        self.response = response

    def __str__(self):
        res = self.response
        return f'RequestError [{res.status_code}]: {res.text}'


class ResponseParseException(Exception):

    def __init__(self, exc: JSONDecodeError, response: Response) -> None:
        super().__init__(exc)
        self.message = exc
        self.response = response

    def __str__(self):
        return f'Response decode error: {self.message}'


class ApiResponseException(RequestFailedException):
    def __init__(self, response: Response, errors) -> None:
        super().__init__(response)
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
