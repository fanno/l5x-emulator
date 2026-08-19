from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Any
from datetime import datetime, timezone

from lxml.etree import _Element as Element

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from core.memory.uimemory import DT
from core.l5k.l5kreader import L5KReader

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.math import MATH
from datatypes.custom.compare import COMPARE
from datatypes.custom.bool import BOOL

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
                chunks.reverse()  # ← ADD THIS FOR LITTLE-ENDIAN
                return f"2#" + "_".join(chunks)
            case "Hex":
                hex_chars = bit_size // 4
                hex_str = format(masked_value, f'0{hex_chars}X')
                # Reverse the chunks (little-endian)
                chunks = [hex_str[i:i+4] for i in range(0, len(hex_str), 4)]
                chunks.reverse()  # ← ADD THIS FOR LITTLE-ENDIAN
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
    
    def __int__(self) -> int:
        return self._value

    def __getitem__(self, bit: int) -> INTIGER_BIT:
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= self.getBitSize():
            raise IndexError(f"Bit index {bit} out of range")

        return INTIGER_BIT(self, bit)

    def __setitem__(self, bit: int, value: bool):
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= self.getBitSize():
            raise IndexError(f"Bit index {bit} out of range")

        current = self.getPLCValue()
        value = BOOL.toValue(value)
        if value:
            old |= 1 << bit
        else:
            old &= ~(1 << bit)

        self.setValue(current)

@dataclass(repr=False, eq=False)
class INTIGER_BIT:
    parent:InitVar[INTIGER]
    bit:InitVar[int]

    _parent:INTIGER = field(init=False, repr=False, default=None)
    _bit:int = field(init=False, repr=False, default=None)

    def __post_init__(self, parent:INTIGER, bit:int) -> None:
        self._parent = parent
        self._bit = bit

    def getPLCValue(self) -> bool:
        current = self._parent.getPLCValue()
        return bool(current & (1 << self._bit))

    def getUAValue(self) -> bool:
        return self.getPLCValue()

    def __bool__(self) -> bool:
        return self.getPLCValue()

    def setValue(self, value: str | int | bool):
        current = self._parent.getPLCValue()

        if BOOL.toValue(value):
            current |= 1 << self._bit
        else:
            current &= ~(1 << self._bit)

        self._parent.setValue(current)

    def __repr__(self):
        return repr(self.getPLCValue())

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

    _value:float = field(init=False, repr=False, default=0.0)
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Float
    _py_variant: ClassVar[type] = float
    _type:ClassVar[DT] = DT.REAL

    def __post_init__(self, init:Any=None) -> None:
        self.setValue(init)

    def getPLCValue(self) -> float:
        return self._value

    def getUAValue(self) -> float:
        return self._value

    def toL5X(self, element:Element) -> None:
        if isinstance(element, Element):
            element.set("Value", str(self._value))

    @staticmethod
    def toValue(value:str|int|float):
        if value is None:
            value = 0.0

        if isPLCInstance(value, SupportsGetPLCValue):
            value = value.getPLCValue()

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
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Double
    _type:ClassVar[DT] = DT.LREAL