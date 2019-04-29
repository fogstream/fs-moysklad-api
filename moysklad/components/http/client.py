from enum import Enum
from time import sleep
from typing import Optional
from urllib.parse import urljoin

from requests import Request, RequestException, Session

from moysklad.components.filters import BaseFilter, Pagination
from moysklad.components.http.options import RequestConfig
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
    def __init__(self, response) -> None:
        self.context = response['context']
        self.meta = response['meta']
        self.rows = response['rows']


class MoySkladHttpClient:
    _endpoint = 'https://online.moysklad.ru/api/remap/1.1/'
    _pos_endpoint = 'https://online.moysklad.ru/api/posap/1.0/'

    def __init__(self, login: str, password: str,
                 pos_token: Optional[str] = None) -> None:
        self._login = login
        self._password = password
        self._pos_token = pos_token
        self._pre_request_sleep_time: float = 200

    def set_pos_token(self, pos_token: str):
        self._pos_token = pos_token

    def get(self, method, data=None, filters=None, options=None):
        return self._make_request(HTTPMethod.GET, method, data, options,
                                  filters=filters)

    def post(self, method, data=None, filters=None, options=None):
        return self._make_request(HTTPMethod.POST, method, data, options,
                                  filters=filters)

    def put(self, method, data=None, filters=None, options=None):
        return self._make_request(HTTPMethod.PUT, method, data, options,
                                  filters=filters)

    def delete(self, method, data=None, filters=None, options=None):
        return self._make_request(HTTPMethod.DELETE, method, data, options,
                                  filters=filters)

    def set_pre_request_timeout(self, ms: float):
        self._pre_request_sleep_time = ms

    # pylint: disable-msg=too-many-locals
    def _make_request(self, http_method: HTTPMethod, api_method, data=None, options=None,
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
                    raise PosTokenException()
                password = self._pos_token
            endpoint = self._pos_endpoint

        headers = {
            'Authorization': f'Basic {get_auth_hash(self._login, password)}',
        }

        config = {
            'method': http_method.value,
            'url': urljoin(endpoint, api_method),
            'headers': headers
        }
        url_params = {}

        if not options.use_pos_api:
            filters = kwargs.get('filters', [])

            for filter_type in filters:
                if issubclass(filter_type.__class__, BaseFilter):
                    url_params[filter_type.name] = filter_type.get_raw()
                elif isinstance(filter_type, Pagination):
                    url_params.update(filter_type.pagination)
                elif isinstance(filter_type, dict):
                    url_params.update(filter_type)
                elif isinstance(filter_type, str) and '=' in filter_type:
                    filter_name, filter_value = filter_type.split('=')
                    url_params[filter_name] = filter_value
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
                return ApiResponse(json_response)
            except ValueError:
                raise ResponseParseException(res)
        except RequestException as e:
            res = e.response
            e = RequestFailedException(e.request, res)
            try:
                res_json = res.json()
                is_list = isinstance(res_json, list)
                errors = res_json[0].get('errors') if is_list else res_json.get('errors')
                if errors:
                    e = ApiResponseException(res.request, res, errors)
            except ValueError:
                pass
            raise e
