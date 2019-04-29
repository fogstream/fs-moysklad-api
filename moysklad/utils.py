from abc import ABCMeta
from base64 import b64encode
from datetime import datetime
import re


MS_TIME_STRING = '%Y-%m-%d %H:%M:%S.%f'
TIME_STRING = '%Y-%m-%d %H:%M:%S'
MS_MATCH = re.compile(r'\.[\d]{3}')


def get_auth_hash(login: str, password: str) -> str:
    return b64encode(f'{login}:{password}'.encode()).decode('utf-8')


def get_time_string(time: datetime, include_ms: bool = False) -> str:
    return (
        time.strftime(MS_TIME_STRING)[:-3]
        if include_ms else
        time.strftime(TIME_STRING)
    )


def parse_time_string(time_string: str) -> datetime:
    if MS_MATCH.fullmatch(time_string):
        date = datetime.strptime(time_string, MS_TIME_STRING)
    else:
        date = datetime.strptime(time_string, TIME_STRING)
    return date


class SingletonABCMeta(ABCMeta):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class AbstractSingleton(metaclass=SingletonABCMeta):
    pass
