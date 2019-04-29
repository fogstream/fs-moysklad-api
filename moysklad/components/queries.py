from abc import ABC, abstractmethod


class BaseQuery(ABC):
    name = 'base'
    _query_buffer = []

    def __init__(self):
        self._query_buffer = []

    @abstractmethod
    def get_raw(self) -> str:
        raise NotImplementedError

    def get_buffer(self):
        return self._query_buffer


class Filter(BaseQuery):
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
        return ';'.join(self._query_buffer)


class Search(BaseQuery):
    name = 'search'

    def __init__(self, query):
        super().__init__()
        self._query_buffer.append(query)

    def get_raw(self) -> str:
        return self._query_buffer[0]


class Ordering(BaseQuery):
    name = 'order'

    def asc(self, field):
        self._query_buffer.append(f'{field},asc')
        return self

    def desc(self, field):
        self._query_buffer.append(f'{field},desc')
        return self

    def get_raw(self):
        return ';'.join(self._query_buffer)


class Expand(BaseQuery):
    name = 'expand'

    def __init__(self, *args):
        super().__init__()
        self._query_buffer.extend(args)

    def get_raw(self):
        return ','.join(self._query_buffer)


class Pagination:
    def __init__(self, limit=25, offset=0):
        self._limit = limit
        self._offset = offset

    @property
    def pagination(self):
        return {
            'limit': self._limit,
            'offset': self._offset,
        }
