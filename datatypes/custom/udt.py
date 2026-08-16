from typing import ClassVar, Callable, Any
from dataclasses import dataclass, fields
from asyncua import ua
from lxml.etree import _Element as Element

from protocols.memory import SupportsSetValue, Resettable, SupportsToL5X, SupportsToUi, SupportsGetPLCValue
from protocols.opcua import SupportsOPCUA, SupportsVariant
from  utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryObject, DT

from opcua.updater import OPCUAU

@dataclass
class UDT(OPCUAU):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.ExtensionObject
    _type:ClassVar[DT] = DT.UDT

    def getUAValue(self) -> ua.Variant:
        dt_name = self.__class__.__name__
        if not hasattr(ua, dt_name):
            if hasattr(ua, dt_name.upper()):
                dt_name = dt_name.upper()
            else:
                dt_name = None

        if dt_name:
            result = getattr(ua, dt_name)()

            for f in fields(self):
                if f.repr:
                    if hasattr(result, f.name):
                        v = getattr(self, f.name);
                        if isPLCInstance(v, SupportsVariant):
                            setattr(result, f.name, v.getUAValue())
                    else:
                        raise ValueError(f"Field class attribute is missing {dt_name}, {f.name}")
            return result
        raise ValueError(f"Classlass {dt_name}, not founed")

    def _reset(self):
        for f in self.__dataclass_fields__.values():
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, Resettable):
                    current._reset()

    def toUI(self, name:str, path_filter: dict[str, dict] | None = None) -> UIMemoryObject:
        members = {}

        for f in self.__dataclass_fields__.values():
            if f.repr:
                if path_filter is None or f.name in path_filter:
                    child = getattr(self, f.name)

                    if isPLCInstance(child, SupportsToUi):
                        next = None
                        if path_filter:
                            next = path_filter[f.name]
                        members[f.name] = child.toUI(f.name, next)

        return UIMemoryObject(name, Class=self.__class__.__name__, Datatype=self._type, Value=members)

    def toL5X(self, element:Element) -> None:
        if isinstance(element , Element):
            for f in self.__dataclass_fields__.values():
                if f.repr:
                    current = getattr(self, f.name, None)

                    if isPLCInstance(current, SupportsToL5X):
                        e = element.find(f'./*[@Name="{f.name}"]')
                        current.toL5X(e)

    def setValue(self, value:"UDT"):
        if type(self).__name__ != type(value).__name__:
            raise TypeError(f"Expected ({type(self)}, {type(self).__name__}), got ({type(value)}, {type(value).__name__})")

        for f in self.__dataclass_fields__.values():
            if f.repr:            
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsSetValue):
                    new_value = getattr(value, f.name, None)
                    current.setValue(new_value)

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        if self._on_change is None:
            self._on_change = on_change

        for f in self.__dataclass_fields__.values():
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsOPCUA):
                    current.setOnChange(self._child_changed)

    def _register_change(self):
        for f in self.__dataclass_fields__.values():
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsOPCUA):
                    current.setOnChange(self._child_changed)