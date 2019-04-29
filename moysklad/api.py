from __future__ import annotations

from typing import Dict, Optional
from zlib import crc32

from moysklad.components.http.client import MoySkladHttpClient


class MoySklad:
    _instances: Dict = {}

    def __init__(self, login: str, password: str, pos_token: str,
                 hash_code: str) -> None:
        self._client = MoySkladHttpClient(login, password, pos_token)
        self._hash_code = hash_code

    @classmethod
    def get_instance(cls, login: str, password: str,
                     pos_token: Optional[str] = None) -> MoySklad:
        hash_code = crc32(f'{login}{password}'.encode()) & 0xffffffff
        if not cls._instances.get(hash_code):
            cls._instances[hash_code] = cls(
                login=login,
                password=password,
                pos_token=pos_token,
                hash_code=hash_code,
            )
        return cls._instances[hash_code]

    @classmethod
    def find_instance_by_hash(cls, hash_code: str) -> MoySklad:
        return cls._instances.get(hash_code)

    @property
    def hash_code(self) -> str:
        return self._hash_code

    def get_client(self) -> MoySkladHttpClient:
        return self._client

    def set_pos_token(self, pos_token) -> None:
        self._client.set_pos_token(pos_token)
