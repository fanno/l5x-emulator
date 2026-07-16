from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.math import MATH
from datatypes.custom.compare import COMPARE

from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64
)

PLC_TYPE_MAP = {
    'SINT': c_int8,
    'USINT': c_uint8,
    'INT': c_int16,
    'UINT': c_uint16,
    'DINT': c_int32,
    'UDINT': c_uint32,
    'LINT': c_int64,
    'ULINT': c_uint64
}

@dataclass(repr=False, eq=False)
class INTIGER(COMPARE, MATH, DataVariant):
    _value:int = field(repr=False, default=0)
    _py_variant:Any = field(init=False, repr=False, default=int)

    def __post_init__(self):
        self.setValue(self._value)

    def setValue(self, value:str|int):
        self._value = self.toValue(value, self.__class__.__name__)

    def getPLCValue(self) -> int:
        return self._value
    
    def getUAValue(self) -> int:
        return self._value
    
    @classmethod
    def toValue(self, value: int, type_name: str):
        value = super().toValue(value)
        if value is None:
            value = 0
        if isinstance(value, str):
            from core.memory import helper
            value = helper.strNumber(value)
        if isinstance(value, bool):
            if value:
                value = 1
            else:
                value = 0

        if not isinstance(value, int):
            value = int(value)

        return PLC_TYPE_MAP[type_name.upper()](value).value
    
    def __int__(self) -> int:
        return self._value

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class ULINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.UInt64)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Int64)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class UDINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.UInt32)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class DINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Int32)


@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class UINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.UInt16)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class INT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Int16)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class USINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Byte)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class SINT(INTIGER):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.SByte)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class REAL(COMPARE, MATH, DataVariant):
    _value:float = field(init=True, repr=False, default=0.0)
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Float)
    _py_variant:Any = field(init=False, repr=False, default=float)

    def __post_init__(self):
        self.setValue(self._value)

    def setValue(self, value:str|float):
        self._value = self.toValue(value)

    def getPLCValue(self) -> float:
        return self._value

    def getUAValue(self) -> float:
        return self._value

    @staticmethod
    def toValue(value:str|int|float):
        if value is None:
            value = 0.0
        if isinstance(value, str):
            from core.memory import helper
            value = helper.strNumber(value)
        if isinstance(value, bool):
            if value:
                value = 1.0
            else:
                value = 0.0
        if not isinstance(value, float):
            value = float(value)

        return float(value)

    def __float__(self) -> float:
        return self._value

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LREAL(REAL):
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Double)