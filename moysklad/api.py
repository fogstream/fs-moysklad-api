from __future__ import annotations

from typing import Optional
from zlib import crc32

from .http import MoySkladHttpClient
from .urls import ApiUrlRegistry


class MoySklad:
    _instances: dict = {}

    def __init__(self, login: str, password: str, pos_token: str,
                 hash_code: str) -> None:
        self._client = MoySkladHttpClient(login, password, pos_token)
        self._methods = ApiUrlRegistry()
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

    def get_methods(self) -> ApiUrlRegistry:
        return self._methods

    def set_pos_token(self, pos_token) -> None:
        self._client.set_pos_token(pos_token)
