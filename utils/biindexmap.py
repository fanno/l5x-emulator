from typing import Dict, TypeVar, Generic, Callable, Optional, Iterator, Type

T = TypeVar('T')

class BiIndexMap(Generic[T]):
    def __init__(self, key1_func: Callable[[T], str], key2_func: Callable[[T], str], expected_type: Optional[Type[T]] = None):
        self._get_key1 = key1_func
        self._get_key2 = key2_func
        
        self._map1: Dict[str, T] = {}
        self._map2: Dict[str, T] = {}

        self._expected_type = expected_type

    def add(self, item: T) -> None:
        if self._expected_type is not None and not isinstance(item, self._expected_type):
            raise TypeError(f"Invalid item type: Expected {self._expected_type.__name__}, "f"but got {type(item).__name__}")
        
        k1 = self._get_key1(item)
        self._map1[k1] = item

        k2 = self._get_key2(item)
        self._map2[k2] = item

    def remove(self, item: T) -> None:
        if self._expected_type is not None and not isinstance(item, self._expected_type):
            raise TypeError(f"Invalid item type: Expected {self._expected_type.__name__}, "f"but got {type(item).__name__}")
        
        k1 = self._get_key1(item)
        self._map1.pop(k1, None)

        k2 = self._get_key2(item)
        self._map2.pop(k2, None)

    def _key(self, key: str|list|tuple) -> str:
        if isinstance(key, (list, tuple)):
            path = []
            for part in key:
                if isinstance(part, int):
                    part = str(part)
                path.append(part)
            key = ".".join(path)
        return key

    def _get_by_first(self, key: str) -> Optional[T]:
        return self._map1.get(self._key(key))

    def _get_by_second(self, key: str) -> Optional[T]:
        return self._map2.get(self._key(key))

    def __iter__(self) -> Iterator[T]:
        return iter(self._map1.values())