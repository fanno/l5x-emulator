from typing import Protocol, runtime_checkable

@runtime_checkable
class Resettable(Protocol):
    def _reset(self) -> None: ...


class UDT:
    def _reset(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isinstance(current, Resettable):
                current._reset()

    def setValue(self):
        raise NotImplementedError(f"{__class__} setValue")