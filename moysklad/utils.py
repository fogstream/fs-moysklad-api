from abc import ABCMeta
from datetime import datetime
import re


TIME_STRING = '%Y-%m-%d %H:%M:%S'
MS_MATCH = re.compile(r'\.[\d]{3}')


class SingletonABCMeta(ABCMeta):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class AbstractSingleton(metaclass=SingletonABCMeta):
    pass


def get_time_string(time: datetime) -> str:
    return time.strftime(TIME_STRING)


def parse_time_string(time_string: str) -> datetime:
    return datetime.strptime(time_string, TIME_STRING)
