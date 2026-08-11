from protocols.memory import SupportsSetValue, Resettable, SupportsToL5X
from  utils.isplcinstance import isPLCInstance

from lxml.etree import _Element as Element

class UDT:
    def _reset(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, Resettable):
                current._reset()

    def toL5X(self, element:Element) -> None:
        if isinstance(element , Element):
            for f in self.__dataclass_fields__.values():
                current = getattr(self, f.name, None)

                if isPLCInstance(current, SupportsToL5X):
                    e = element.find(f'./*[@Name="{f.name}"]')
                    current.toL5X(e)

    def setValue(self, value:"UDT"):
        if type(value) is not type(self):
            raise TypeError(f"Expected {type(self).__name__}, got {type(value).__name__}")

        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, SupportsSetValue):
                new_value = getattr(value, f.name, None)
                if new_value is not None:
                    current.setValue(new_value)