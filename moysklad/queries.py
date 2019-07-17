from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union

from .utils import get_time_string


class Query:
    def __init__(self, *args) -> None:
        self._url_params = {}
        for query in args:
            if isinstance(query, BaseQuery):
                self._url_params[query.name] = query.get_raw()
            elif isinstance(query, Select):
                self._url_params.update(query.spec)
            elif isinstance(query, dict):
                self._url_params.update(query)
            elif isinstance(query, str) and '=' in query:
                query_name, query_value = query.split('=')
                self._url_params[query_name] = query_value
            elif isinstance(query, Query):
                self._url_params.update(query.url_params)
            else:
                raise NotImplementedError('Unsupported filter type')

    @property
    def url_params(self):
        return self._url_params


class BaseQuery(ABC):
    name = 'base'

    def __init__(self):
        self._query_buffer = []

    @abstractmethod
    def get_raw(self) -> str:
        raise NotImplementedError

    def get_buffer(self):
        return set(self._query_buffer)

    def __str__(self) -> str:
        filter_str = ', '.join(self._query_buffer)
        return f'{self.name.capitalize()}({filter_str})'


class Filter(BaseQuery):
    """
    Конструктор фильтров
    https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%D0%BA%D0%B8-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%B0-filter
    """
    name = 'filter'

    def eq(self, field, value):
        self._query_buffer.append(f'{field}={value}')
        return self

    def neq(self, field, value):
        self._query_buffer.append(f'{field}!={value}')
        return self

    def gt(self, field, value):
        self._query_buffer.append(f'{field}>{value}')
        return self

    def lt(self, field, value):
        self._query_buffer.append(f'{field}<{value}')
        return self

    def gte(self, field, value):
        self._query_buffer.append(f'{field}>={value}')
        return self

    def lte(self, field, value):
        self._query_buffer.append(f'{field}<={value}')
        return self

    def like(self, field, value):
        self._query_buffer.append(f'{field}~{value}')
        return self

    def st(self, field, value):
        self._query_buffer.append(f'{field}~={value}')
        return self

    def et(self, field, value):
        self._query_buffer.append(f'{field}=~{value}')
        return self

    def in_(self, field, values):
        equals = [f'{field}={value}' for value in values]
        self._query_buffer.append(f';'.join(equals))
        return self

    def nin_(self, field, values):
        equals = [f'{field}!={value}' for value in values]
        self._query_buffer.append(f';'.join(equals))
        return self

    def exists(self, field, exists=True):
        operator = '!=' if exists else '='
        self._query_buffer.append(f'{field}{operator}')
        return self

    def get_raw(self):
        return ';'.join(set(self._query_buffer))

    def __add__(self, other: Filter):
        queries = set(self._query_buffer) ^ set(other._query_buffer)
        new_filter = self.__class__()
        new_filter._query_buffer = list(queries)
        return new_filter


class Search(BaseQuery):
    """
    Контекстный поиск
    https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D1%8B%D0%B9-%D0%BF%D0%BE%D0%B8%D1%81%D0%BA
    """
    name = 'search'

    def __init__(self, query):
        super().__init__()
        self._query_buffer.append(query)

    def get_raw(self) -> str:
        return self._query_buffer[0]


class Ordering(BaseQuery):
    """
    Сортировка объектов
    https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2
    """
    name = 'order'

    def asc(self, field):
        self._query_buffer.append(f'{field},asc')
        return self

    def desc(self, field):
        self._query_buffer.append(f'{field},desc')
        return self

    def get_raw(self):
        return ';'.join(set(self._query_buffer))


class Expand(BaseQuery):
    """
    Раскрытие вложенных сущностей
    https://online.moysklad.ru/api/remap/1.1/doc/index.html#%D0%BE%D0%B1%D1%89%D0%B8%D0%B5-%D1%81%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0-%D1%81%D1%81%D1%8B%D0%BB%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-expand
    """
    name = 'expand'

    def __init__(self, *args):
        super().__init__()
        for entity_name in args:
            if len(entity_name.split('.')) <= 3:
                self._query_buffer.append(entity_name)

    def get_raw(self):
        return ','.join(self._query_buffer)


class Select:
    MAX_LIST_LIMIT = 1000

    def __init__(
            self,
            limit: int = 100, offset: int = 0,
            updated_from: Optional[Union[datetime, str]] = None,
            updated_to: Optional[Union[datetime, str]] = None,
            updated_by: Optional[str] = None,
            additional: Optional[dict] = None,
    ):
        self._limit = limit if limit <= self.MAX_LIST_LIMIT else self.MAX_LIST_LIMIT
        self._offset = offset
        self._updated_by = updated_by
        self._additional = additional or {}

        if isinstance(updated_from, datetime):
            self._updated_from = get_time_string(updated_from)
        else:
            self._updated_from = updated_from

        if isinstance(updated_to, datetime):
            self._updated_to = get_time_string(updated_to)
        else:
            self._updated_to = updated_to

    def limit(self, limit):
        self._limit = limit
        return self

    def offset(self, offset):
        self._offset = offset
        return self

    @property
    def spec(self):
        params = {
            'limit': self._limit,
            'offset': self._offset,
            'updatedFrom': self._updated_from,
            'updatedTo': self._updated_to,
            'updatedBy': self._updated_by,
        }
        params.update(self._additional)
        return params
