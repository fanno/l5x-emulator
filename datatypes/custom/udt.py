from typing import ClassVar, Callable, Any
from dataclasses import dataclass, fields
from asyncua import ua
from lxml.etree import _Element as Element

from protocols.memory import SupportsSetValue, Resettable, SupportsToL5X, SupportsToUi, SupportsGetPLCValue
from protocols.opcua import SupportsOPCUA, SupportsVariant
from  utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryObject, DT

from opcua.updater import OPCUAU

from datatypes.custom.l5k import L5K
from datatypes.custom.bool import BOOL

from core.l5k.l5kreader import L5KSKIP_KEY, L5KBOOLBYTEEND_KEY

@dataclass
class UDT(OPCUAU, L5K):
    _l5k_bool_bit: ClassVar[int] = 0
    _l5k_bool_step: ClassVar[int] = 1
    _l5k_bool_end: ClassVar[int] = 7

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
        for f in fields(self):
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, Resettable):
                    current._reset()

    def toUI(self, name:str, path_filter: dict[str, dict] | None = None) -> UIMemoryObject:
        members = {}

        for f in fields(self):
            if f.repr:
                showInUI = True
                if f.metadata.get("usage") == "Local":
                    showInUI = False

                if showInUI:
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
            for f in fields(self):
                if f.repr:
                    current = getattr(self, f.name, None)

                    if isPLCInstance(current, SupportsToL5X):
                        e = element.find(f'./*[@Name="{f.name}"]')
                        current.toL5X(e)

    def setValue(self, value:"UDT"):
        if type(self).__name__ != type(value).__name__:
            raise TypeError(f"Expected ({type(self)}, {type(self).__name__}), got ({type(value)}, {type(value).__name__})")

        for f in fields(self):
            if f.repr:            
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsSetValue):
                    new_value = getattr(value, f.name, None)
                    current.setValue(new_value)

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        if self._on_change is None:
            self._on_change = on_change

        for f in fields(self):
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsOPCUA):
                    current.setOnChange(self._child_changed)

    def _register_change(self):
        for f in fields(self):
            if f.repr:
                current = getattr(self, f.name, None)
                if isPLCInstance(current, SupportsOPCUA):
                    current.setOnChange(self._child_changed)

    def fromL5K(self, data):
        from datatypes.custom.array import Array
        from datatypes.custom.string import STRING
        
        reader = self.getReader(data)

        if isinstance(self, UDT):
            reader.setBitRules(self._l5k_bool_bit, self._l5k_bool_step, self._l5k_bool_end)

        for field in fields(self):
            if not field.repr:
                continue
            
            value = getattr(self, field.name)

            if not field.metadata.get(L5KSKIP_KEY, False):
                if isinstance(value, BOOL):
                    value.setValue(reader.nextBool())
                    if field.metadata.get(L5KBOOLBYTEEND_KEY, False):
                        reader.nextBoolByte()                    
                elif isinstance(value, Array):
                    value.fromL5K(reader.nextRaw())
                elif isinstance(value, STRING):
                    string = reader.nextRaw()
                    value.fromL5K(string)
                elif isinstance(value, UDT):
                    value.fromL5K(reader.nextRaw())
                else:
                    value.setValue(reader.nextRaw())

@dataclass
class _R32BIT_UDT(UDT):
    _l5k_bool_bit: ClassVar[int] = 31
    _l5k_bool_step: ClassVar[int] = -1
    _l5k_bool_end: ClassVar[int] = 0

@dataclass
class _32BIT_UDT(UDT):
    _l5k_bool_bit: ClassVar[int] = 0
    _l5k_bool_step: ClassVar[int] = 1
    _l5k_bool_end: ClassVar[int] = 31
    