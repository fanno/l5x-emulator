from contextlib import contextmanager

class Hierarchy:
    _items: list[str] = []

    @classmethod
    def add(cls, text: str) -> int:
        cls._items.append(text)
        return len(cls._items)

    @classmethod
    def collapse(cls, level: int) -> None:
        if level <= 0:
            cls._items.clear()
        else:
            del cls._items[level - 1:]

    @classmethod
    def current(cls) -> tuple[str, ...]:
        return tuple(cls._items)

    @classmethod
    @contextmanager
    def scope(cls, text: str):
        cls._items.append(text)
        try:
            yield
        finally:
            cls._items.pop()

    @classmethod
    def path(cls, separator: str = "->") -> str:
        return separator.join(cls._items)