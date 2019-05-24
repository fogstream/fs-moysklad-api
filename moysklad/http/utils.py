from enum import Enum
from typing import Optional

from requests import Response


DEBUG_RATE_HEADERS = {
    'X-RateLimit-Limit': 'true',
    'X-Lognex-Retry-TimeInterval': 'true',
    'X-RateLimit-Remaining': 'true',
    'X-Lognex-Reset': 'true',
    'X-Lognex-Retry-After': 'true',
}


class HTTPMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


class ApiResponse:
    def __init__(self, response: Response, json_response: dict) -> None:
        self.data = json_response

        if isinstance(json_response, dict):
            self.context = json_response.get('context')
            self.meta = json_response.get('meta')
            self.rows = json_response.get('rows')
        else:
            self.context = None
            self.meta = None
            self.rows = json_response

        self.response = response
        self.headers = response.headers

    def __str__(self):
        return f'ApiResponse [{self.response.status_code}]'


class RequestConfig:
    def __init__(
            self, use_pos_api: bool = False,
            use_pos_token: bool = False,
            ignore_request_body: bool = False,
            follow_redirects: bool = True,
            format_millisecond: bool = False,
            debug_rate_limit: bool = False,
            disable_webhooks_dispatch: bool = True,
            custom_headers: Optional[dict] = None,
    ) -> None:
        self.use_pos_api = use_pos_api
        self.use_pos_token = use_pos_token
        self.ignore_request_body = ignore_request_body
        self.follow_redirects = follow_redirects
        self.format_millisecond = format_millisecond
        self.debug_rate_limit = debug_rate_limit
        self.disable_webhooks_dispatch = disable_webhooks_dispatch
        self.custom_headers = custom_headers
