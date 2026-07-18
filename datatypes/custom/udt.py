from typing import Protocol, runtime_checkable

@runtime_checkable
class Resettable(Protocol):
    def __reset(self) -> None: ...


class UDT:
    def __reset(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isinstance(current, Resettable):
                current.__reset()