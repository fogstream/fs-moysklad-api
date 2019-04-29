MoySklad
===========

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

### Пагинация
```python
Pagination(limit=1, offset=0)
```
[Документация](https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D0%BC%D0%B5%D1%82%D0%B0%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5)

## Примеры кода
Авторизация и получения контрагентов с применением фильтрации
```python
from moysklad.api import MoySklad
from moysklad.queries import Expand, Filter, Ordering, Pagination, Search


sklad = MoySklad.get_instance('login', 'password')
client = sklad.get_client()
methods = sklad.get_methods()

data = client.get(
    method=methods.get_list_url('counterparty'),
    queries=[
        Filter().exists('email').eq('archived', False),
        Search('петров'),
        Expand('owner', 'owner.group'),
        Ordering().asc('id').desc('name'),
        Pagination(1),
    ],
)
print(data.meta)
print(data.context)
print(data.rows[0])

```