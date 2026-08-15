from typing import ClassVar, Callable, Any, Set, TYPE_CHECKING
from dataclasses import dataclass, field
from asyncua import ua
from lxml.etree import _Element as Element

from protocols.memory import SupportsSetValue, Resettable, SupportsToL5X, SupportsToUi, SupportsGetPLCValue
from protocols.opcua import SupportsOPCUA
from  utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryObject, DT
if TYPE_CHECKING:
    from core.signal import Signal
    from core.memory.memory import Memory

from opcua.updater import OPCUAU

@dataclass
class UDT(OPCUAU):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.ExtensionObject
    _type:ClassVar[DT] = DT.UDT

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

        changed = False
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, SupportsSetValue|SupportsGetPLCValue):
                new_value = getattr(value, f.name, None)

                if isPLCInstance(current, SupportsGetPLCValue) and isPLCInstance(new_value, SupportsGetPLCValue):
                    if current.getPLCValue() != new_value.getPLCValue():
                        changed = True
                        current.setValue(new_value)
                if new_value is not None:
                    changed = False
                    current.setValue(new_value)
        if changed:
            self._notify_change()

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        if self._on_change is None:
            self._on_change = on_change

        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, SupportsOPCUA):
                current.setOnChange(self._child_changed)

    def _register_change(self):
        for f in self.__dataclass_fields__.values():
            current = getattr(self, f.name, None)
            if isPLCInstance(current, SupportsOPCUA):
                current.setOnChange(self._child_changed)