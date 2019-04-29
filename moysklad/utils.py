from abc import ABCMeta
from base64 import b64encode
import datetime


def get_auth_hash(login: str, password: str) -> str:
    return b64encode(f'{login}:{password}'.encode()).decode('utf-8')


def format_time(time: datetime.datetime) -> str:
    return time.strftime('Y-m-d H:i:s')


class SingletonABCMeta(ABCMeta):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(
                SingletonABCMeta, cls).__call__(*args, **kwargs)

        return cls._instance


class AbstractSingleton(metaclass=SingletonABCMeta):
    pass
