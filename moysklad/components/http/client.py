from enum import Enum
from time import sleep
from typing import Dict, List, Optional
from urllib.parse import urljoin

from requests import Request, RequestException, Session

from moysklad.components.http.options import RequestConfig
from moysklad.components.queries import BaseQuery, Pagination
from moysklad.exceptions import (
    ApiResponseException,
    PosTokenException,
    RequestFailedException,
    ResponseParseException,
)
from moysklad.utils import get_auth_hash


class HTTPMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'


JSON_REQUEST_TYPES = (HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE)


class ApiResponse:
    def __init__(self, response, json_response) -> None:
        self.context = json_response['context']
        self.meta = json_response['meta']
        self.rows = json_response['rows']
        self.response = response
        self.headers = response.headers

    def __str__(self):
        return f'ApiResponse [{self.response.status_code}]'


class MoySkladHttpClient:
    _endpoint = 'https://online.moysklad.ru/api/remap/1.1/'
    _pos_endpoint = 'https://online.moysklad.ru/api/posap/1.0/'

    def __init__(self, login: str, password: str,
                 pos_token: Optional[str] = None) -> None:
        self._login = login
        self._password = password
        self._pos_token = pos_token
        self._pre_request_sleep_time: float = 200

    def set_pos_token(self, pos_token: str) -> None:
        self._pos_token = pos_token

    def get(self, method: str,
            data: Dict = None,
            queries: Optional[List] = None,
            options: Optional[RequestConfig] = None):
        return self._make_request(
            http_method=HTTPMethod.GET,
            api_method=method,
            data=data,
            options=options,
            queries=queries,
        )

    def post(self, method: str,
             data: Dict = None,
             queries: Optional[List] = None,
             options: Optional[RequestConfig] = None):
        return self._make_request(
            http_method=HTTPMethod.POST,
            api_method=method,
            data=data,
            options=options,
            queries=queries,
        )

    def put(self, method: str,
            data: Dict = None,
            queries: Optional[List] = None,
            options: Optional[RequestConfig] = None):
        return self._make_request(
            http_method=HTTPMethod.PUT,
            api_method=method,
            data=data,
            options=options,
            queries=queries,
        )

    def delete(self, method: str,
               data: Dict = None,
               queries: Optional[List] = None,
               options: Optional[RequestConfig] = None):
        return self._make_request(
            http_method=HTTPMethod.DELETE,
            api_method=method,
            data=data,
            options=options,
            queries=queries,
        )

    def set_pre_request_timeout(self, ms: float) -> None:
        self._pre_request_sleep_time = ms

    # pylint: disable-msg=too-many-locals
    def _make_request(self, http_method: HTTPMethod, api_method: str,
                      data=None, options: Optional[RequestConfig] = None,
                      **kwargs):
        if not data:
            data = {}
        if not options:
            options = RequestConfig()

        password = self._password
        endpoint = self._endpoint

        if options.use_pos_api:
            if options.use_pos_token:
                if not self._pos_token:
                    raise PosTokenException('POS token is used, but it\'s invalid or empty')
                password = self._pos_token
            endpoint = self._pos_endpoint

        headers = {
            'Authorization': f'Basic {get_auth_hash(self._login, password)}',
        }
        if options.format_millisecond:
            headers['X-Lognex-Format-Millisecond'] = 'true'
        if options.debug_rate_limit:
            debug_rate_headers = {
                'X-RateLimit-Limit': 'true',
                'X-Lognex-Retry-TimeInterval': 'true',
                'X-RateLimit-Remaining': 'true',
                'X-Lognex-Reset': 'true',
                'X-Lognex-Retry-After': 'true',
            }
            headers.update(debug_rate_headers)

        config = {
            'method': http_method.value,
            'url': urljoin(endpoint, api_method),
            'headers': headers
        }

        url_params = {}
        if not options.use_pos_api:
            queries = kwargs.get('queries', [])

            for query in queries:
                if isinstance(query, BaseQuery):
                    url_params[query.name] = query.get_raw()
                elif isinstance(query, Pagination):
                    url_params.update(query.pagination)
                elif isinstance(query, dict):
                    url_params.update(query)
                elif isinstance(query, str) and '=' in query:
                    query_name, query_value = query.split('=')
                    url_params[query_name] = query_value
                else:
                    raise NotImplementedError('Unsupported filter type')

        request_body = {
            'params': url_params,
        }
        if not options.ignore_request_body:
            if http_method == HTTPMethod.GET:
                request_body['params'].update(data)
            elif http_method in JSON_REQUEST_TYPES:
                request_body['json'] = data
            else:
                raise NotImplementedError('Unsupported request type')

        session = Session()
        request = Request(**config, **request_body)
        prepared = session.prepare_request(request)

        try:
            sleep(self._pre_request_sleep_time / 1000)

            res = session.send(
                request=prepared,
                allow_redirects=options.follow_redirects,
            )
            res.raise_for_status()

            if http_method == HTTPMethod.DELETE:
                return None

            if not options.follow_redirects and res.is_redirect:
                return res.headers.get('location', '')

            try:
                json_response = res.json()
                return ApiResponse(res, json_response)
            except ValueError:
                raise ResponseParseException(res)
        except RequestException as e:
            res = e.response
            e = RequestFailedException(res)
            try:
                res_json = res.json()
                is_list = isinstance(res_json, list)
                errors = res_json[0].get('errors') if is_list else res_json.get('errors')
                if errors:
                    e = ApiResponseException(res, errors)
            except ValueError:
                pass
            raise e
