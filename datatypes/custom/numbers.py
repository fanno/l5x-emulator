from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Any, Iterator
from datetime import datetime, timezone

import struct
import math

from lxml.etree import _Element as Element

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from core.memory.uimemory import DT

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.math import MATH
from datatypes.custom.compare import COMPARE
from datatypes.custom.bool import BOOL, MEMORY_BIT

from protocols.memory import SupportsGetPLCValue

from utils.isplcinstance import isPLCInstance
from ctypes import sizeof
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
    init: InitVar[Any] = None

    _value:int = field(init=False, repr=False, default=0)
    _py_variant: ClassVar[type] = int

    def __post_init__(self, init:Any=None) -> None:
        self.setValue(init)

    def setValue(self, value:str|int):
        old = self._value
        self._value = self.toValue(value, self.__class__.__name__)

        if old != self._value:
            self._notify_change()

    def getPLCValue(self) -> int:
        return self._value
    
    def getUAValue(self) -> int:
        return self._value
    
    def getBitSize(self) -> int:
        return sizeof(PLC_TYPE_MAP[self.__class__.__name__]) * 8

    def _format_radix_value(self, value, radix: str) -> str:
        bit_size = self.getBitSize()
        mask = (1 << bit_size) - 1
        masked_value = value & mask

        match radix:
            case "Binary":
                binary = format(masked_value, f'0{bit_size}b')
                chunks = [binary[i:i+4] for i in range(0, len(binary), 4)]
                chunks.reverse()
                return f"2#" + "_".join(chunks)
            case "Hex":
                hex_chars = bit_size // 4
                hex_str = format(masked_value, f'0{hex_chars}X')
                chunks = [hex_str[i:i+4] for i in range(0, len(hex_str), 4)]
                chunks.reverse()
                return f"16#" + "_".join(chunks)
            case "Decimal":
                return str(masked_value)
            case "Date/Time":
                dt = datetime.fromtimestamp(masked_value, tz=timezone.utc)
                micros_formatted = f"{dt.microsecond // 1000:03d}_{dt.microsecond % 1000:03d}"
                return f"DT#{dt.strftime('%Y-%m-%d-%H:%M:%S')}.{micros_formatted}Z"
            case "ASCII":
                num_bytes = bit_size // 8
                byte_data = masked_value.to_bytes(num_bytes, byteorder='big')
                hex_parts = [f"${b:02X}" for b in byte_data]
                return "'" + "".join(hex_parts) + "'"
            case _:
                raise NotImplementedError(f"{self.__class__.__name__}.toL5X radix={radix!r} not implemented")

    def toL5X(self, element:Element) -> None:
        if isinstance(element, Element):
            radix = element.get("Radix", None)
            if radix is not None:
                formatted = self._format_radix_value(self._value, radix)
                element.set("Value", formatted)

    @classmethod
    def toValue(cls, value: int, type_name: str):
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

    def __len__(self) -> int:
        return self.getBitSize()
    
    def __int__(self) -> int:
        return self._value

    def __iter__(self) -> Iterator[MEMORY_BIT]:
        for bit_index in range(len(self)):
            yield self[bit_index]

    def __getitem__(self, bit: int) -> MEMORY_BIT:
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= self.getBitSize():
            raise IndexError(f"Bit index {bit} out of range")

        return MEMORY_BIT(self, bit)

    def __setitem__(self, bit: int, value: bool):
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= self.getBitSize():
            raise IndexError(f"Bit index {bit} out of range")

        current = self.getPLCValue()
        if BOOL.toValue(value):
            old |= 1 << bit
        else:
            old &= ~(1 << bit)

        self.setValue(current)

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class ULINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.UInt64
    _type:ClassVar[DT] = DT.ULINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Int64
    _type:ClassVar[DT] = DT.LINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class UDINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.UInt32
    _type:ClassVar[DT] = DT.UDINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class DINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Int32
    _type:ClassVar[DT] = DT.DINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class UINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.UInt16
    _type:ClassVar[DT] = DT.UINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class INT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Int16
    _type:ClassVar[DT] = DT.INT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class USINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Byte
    _type:ClassVar[DT] = DT.USINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class SINT(INTIGER):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.SByte
    _type:ClassVar[DT] = DT.SINT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class REAL(COMPARE, MATH, DataVariant):
    init: InitVar[Any] = None

    _value: float = field(init=False, repr=False, default=0.0)
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Float
    _py_variant: ClassVar[type] = float
    _type: ClassVar[DT] = DT.REAL

    FOFRMAT: ClassVar[float] = 'f'
    PRECISION_EPSILON: ClassVar[float] = 1e-6
    CLAMP_MIN: ClassVar[float] = -3.40282347e+38
    CLAMP_MAX: ClassVar[float] = 3.40282347e+38
    ALLOW_SPECIAL_VALUES: ClassVar[bool] = True

    def __post_init__(self, init: Any = None) -> None:

        self.setValue(init)

    def getPLCValue(self) -> float:
        return self._value

    def getUAValue(self) -> float:
        return self._value

    def _clamp(self, value: float) -> float:
        if math.isnan(value):
            if self.ALLOW_SPECIAL_VALUES:
                return value
            raise ValueError(f"NaN not allowed for {self.__class__.__name__} type")
        
        if math.isinf(value):
            if self.ALLOW_SPECIAL_VALUES:
                return value
            raise ValueError(f"Infinity not allowed for {self.__class__.__name__} type")
        
        if value > self.CLAMP_MAX:
            value = self.CLAMP_MAX
        elif value < self.CLAMP_MIN:
            value = self.CLAMP_MIN
        
        try:
            packed = struct.pack(self.FOFRMAT, value)
            reconstructed = struct.unpack(self.FOFRMAT, packed)[0]
            
            if abs(value - reconstructed) > abs(value) * self.PRECISION_EPSILON:
                value = reconstructed
            
            return value
        except (struct.error, OverflowError) as e:
            raise ValueError(f"Value {value} exceeds {self.__class__.__name__} representation: {e}")

    def toL5X(self, element: Element) -> None:
        if isinstance(element, Element):
            element.set("Value", str(self._value))

    def toValue(self, value: str | int | float) -> float:
        if value is None:
            value = 0.0

        if isPLCInstance(value, SupportsGetPLCValue):
            value = value.getPLCValue()

        if isinstance(value, str):
            from core.memory import helper
            value = helper.strNumber(value)
        if isinstance(value, bool):
            value = 1.0 if value else 0.0

        if not isinstance(value, float):
            value = float(value)
            
        value = self._clamp(value)
        return value

    def __float__(self) -> float:
        return self._value

    def __repr__(self) -> str:
        return repr(self.getPLCValue())

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LREAL(REAL):
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Double
    _type: ClassVar[DT] = DT.LREAL

    FOFRMAT: ClassVar[float] = 'd'
    PRECISION_EPSILON: ClassVar[float] = 1e-14
    CLAMP_MIN: ClassVar[float] = -1.7976931348623157e+308
    CLAMP_MAX: ClassVar[float] = 1.7976931348623157e+308