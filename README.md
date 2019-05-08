MoySklad
===========

[![PyPI Version](https://img.shields.io/pypi/v/fs-moysklad-api.svg)](https://pypi.python.org/pypi/fs-moysklad-api)

Описание
------------
Библиотека упрощающая работу с API [МойСклад](https://www.moysklad.ru/).


Возможности
-----------
* Конструктор фильтров и запросов
* Репозиторй API эндпоинтов
* Возможность работы с JSON и POS API

## Конструктор запросов
### Фильтрация
```python
Filter().exists('email').eq('archived', False).exists('name', False)
```
Комбинирование фильтров
 ```python
 new_filter = Filter().exists('email') + Filter().exists('name', False)
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%D0%BA%D0%B8-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D0%B0-filter) по фильтрам

### Сортировка
```python
Ordering().asc('id').desc('name')
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2) сортировки

### Контекстный поиск
```python
Search('петров')
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D1%8B%D0%B9-%D0%BF%D0%BE%D0%B8%D1%81%D0%BA) контекстного поиска


### Раскрытие вложенных сущностей
```python
Expand('owner', 'owner.group', 'state')
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#%D0%BE%D0%B1%D1%89%D0%B8%D0%B5-%D1%81%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0-%D1%81%D1%81%D1%8B%D0%BB%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-expand)

### Параметры фильтрации выборки
```python
Select(limit=1, offset=0, updated_to=datetime.now(), updated_by='uuid')
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D0%BF%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D1%8B-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D1%86%D0%B8%D0%B8-%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%D0%BA%D0%B8)

## Примеры кода
Авторизация и получения контрагентов с применением фильтрации
```python
from moysklad.api import MoySklad
from moysklad.queries import Expand, Filter, Ordering, Select, Search, Query


sklad = MoySklad.get_instance('login', 'password')
client = sklad.get_client()
methods = sklad.get_methods()

response = client.get(
    method=methods.get_list_url('counterparty'),
    query=Query(
        Filter().exists('email').eq('archived', False),
        Search('петров'),
        Expand('owner', 'owner.group'),
        Ordering().asc('id').desc('name'),
        Select(limit=1),
    ),
)
print(response.meta)
print(response.context)
print(response.rows[0])

```

## Использование прокси
```python
sklad = MoySklad.get_instance('login', 'password')
client = sklad.get_client()

proxies = {
    'http': 'type://user:pass@host:port',
    'https:': 'type://user:pass@host:port',
}
client.set_proxies(proxies)
```
Для использования [SOCKS5](https://ru.wikipedia.org/wiki/SOCKS#%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB_SOCKS_5) прокси необходимо установить библиотеку [PySocks](https://github.com/Anorov/PySocks).