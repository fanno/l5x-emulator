from typing import Protocol, runtime_checkable


from protocols.memory import SupportsSetValue
from  utils.isplcinstance import isPLCInstance

from protocols.memory import Resettable

class UDT:
    def _reset(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, Resettable):
                current._reset()

    def setValue(self, value:"UDT"):
        if type(value) is not type(self):
            raise TypeError(f"Expected {type(self).__name__}, got {type(value).__name__}")

        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, SupportsSetValue):
                new_value = getattr(value, f.name, None)
                if new_value is not None:
                    current.setValue(new_value)