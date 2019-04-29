from abc import ABC, abstractmethod


class BaseQuery(ABC):
    name = 'base'

    def __init__(self):
        self._query_buffer = []

    @abstractmethod
    def get_raw(self) -> str:
        raise NotImplementedError

    def get_buffer(self):
        return self._query_buffer


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
        return ';'.join(self._query_buffer)


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
        return ';'.join(self._query_buffer)


class Expand(BaseQuery):
    """
    Раскрытие вложенных сущностей

    https://online.moysklad.ru/api/remap/1.1/doc/index.html#%D0%BE%D0%B1%D1%89%D0%B8%D0%B5-%D1%81%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0-%D1%81%D1%81%D1%8B%D0%BB%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-expand
    """
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
