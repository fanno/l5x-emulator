from dataclasses import dataclass, field

from protocols.memory import SupportsSetValue, Resettable, SupportsToL5X, SupportsToUi
from  utils.isplcinstance import isPLCInstance

from lxml.etree import _Element as Element

from core.memory.uimemory import UIMemoryObject, DT

@dataclass
class UDT:
    _type:DT = field(init=False, repr=False, default=DT.UDT)

    def _reset(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, Resettable):
                current._reset()

    def toUI(self, name:str, path_filter: dict[str, dict] | None = None) -> UIMemoryObject:
        members = {}

        for field_name in self.__dataclass_fields__:
            if path_filter is None or field_name in path_filter:
                child = getattr(self, field_name)

                if isPLCInstance(child, SupportsToUi):
                    next = None
                    if path_filter:
                        next = path_filter[field_name]
                    members[field_name] = child.toUI(field_name, next)

        return UIMemoryObject(name, Class=self.__class__.__name__, Datatype=self._type, Value=members)

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