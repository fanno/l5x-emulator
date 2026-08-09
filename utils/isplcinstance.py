from typing import TypeGuard, TypeVar

T = TypeVar("T")

from functools import lru_cache

@lru_cache(maxsize=None)
def isPLCSubclass(cls: type, expected: type) -> bool:
    return issubclass(cls, expected)

def isPLCInstance(obj: object, cls: type[T], ) -> TypeGuard[T]:
    return isPLCSubclass(type(obj), cls)