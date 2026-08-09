from typing import Callable, Generic, Iterator, Optional, Type, TypeVar, Hashable

T = TypeVar("T")

class IndexMap(Generic[T]):
    def __init__(self, expected_type: Optional[Type[T]] = None):
        self._indexes: list[dict[Hashable, T]] = []
        self._key_funcs: list[Callable[[T], Hashable]] = []

        self._expected_type = expected_type

    def _addIndex(self, key_func: Callable[[T], Hashable] ) -> int:
        self._key_funcs.append(key_func)
        self._indexes.append({})

        return len(self._indexes) - 1

    def add(self, item: T) -> None:
        if (self._expected_type is not None and not isinstance(item, self._expected_type)):
            raise TypeError(f"Invalid item type: Expected {self._expected_type.__name__}, but got {type(item).__name__}")

        keys = [key_func(item) for key_func in self._key_funcs]

        for key, index in zip(keys, self._indexes):
            if key is not None:
                index[key] = item

    def remove(self, item: T) -> None:
        if (self._expected_type is not None and not isinstance(item, self._expected_type)):
            raise TypeError(f"Invalid item type: Expected {self._expected_type.__name__}, but got {type(item).__name__}")

        for key_func, index in zip(self._key_funcs, self._indexes):
            key = key_func(item)
            index.pop(key, None)

    def _key(self, key: str | list | tuple ) -> str:
        if isinstance(key, (list, tuple)):
            path = []

            for part in key:
                if isinstance(part, int):
                    part = str(part)

                path.append(part)

            key = ".".join(path)

        return key

    def get(self, index: int, key: Hashable ) -> Optional[T]:
        if index >= len(self._indexes):
            raise IndexError(f"Index {index} does not exist")

        if isinstance(key, (list, tuple)):
            key = self._key(key)

        return self._indexes[index].get(key)

    def __iter__(self) -> Iterator[T]:
        return iter(self._indexes[0].values())