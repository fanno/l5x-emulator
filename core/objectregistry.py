import logging

from typing import Type, TypeVar

T = TypeVar("T")
class ObjectRegistry:
    _data: dict[int, object] = {}

    @staticmethod
    def get(obj, factory: Type[T]) -> T:
        key = ObjectRegistry._key(obj)

        if key not in ObjectRegistry._data:
            logging.debug(f"create new object: {key}")
            ObjectRegistry._data[key] = factory()
        return ObjectRegistry._data[key]

    @staticmethod
    def has(obj) -> bool:
        key = ObjectRegistry._key(obj)
        return key in ObjectRegistry._data

    @staticmethod
    def remove(obj):
        key = ObjectRegistry._key(obj)
        ObjectRegistry._data.pop(key, None)

    @staticmethod
    def _key(obj) -> int:
        try:
            return hash(obj)
        except TypeError:
            return id(obj)