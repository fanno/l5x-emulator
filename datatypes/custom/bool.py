import struct
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Any, Type, TYPE_CHECKING

from lxml.etree import _Element as Element

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.compare import COMPARE
if TYPE_CHECKING:
    from datatypes.custom.numbers import REAL, LREAL

from core.memory.uimemory import DT

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class BOOL(COMPARE, DataVariant):
    init: InitVar[Any] = None
    _value:bool = field(init=False, repr=False, default=False)
    _type: ClassVar[DT] = DT.BOOL
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Boolean
    _py_variant: ClassVar[type] = bool

    def __post_init__(self, init:Any=None) -> None:
        self.setValue(init)

    def getPLCValue(self) -> bool:
        return self._value
    
    def getUAValue(self) -> bool:
        return self._value
    
    def __bool__(self) -> bool:
        return self._value

    def toL5X(self, element:Element) -> None:
        if isinstance(element, Element):
            if self._value:
                element.set("Value", "1")
            else:
                element.set("Value", "0")

    @classmethod
    def toValue(cls, value:str|int|bool) -> bool:
        value = super().toValue(value)
        if isinstance(value, str):
            value = value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(value, int):
            value = value > 0

        if not isinstance(value, bool):
            value = bool(value)
            
        return value
    
@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class BIT(BOOL):
    _type: ClassVar[DT] = DT.BIT

@dataclass(repr=False, eq=False)
class MEMORY_BIT:
    parent:InitVar[Type]
    bit:InitVar[int]

    _parent:Type = field(init=False, repr=False, default=None)
    _bit:int = field(init=False, repr=False, default=None)

    def __post_init__(self, parent:Type, bit:int) -> None:
        self._parent = parent
        self._bit = bit

    def getPLCValue(self) -> bool:
        current = self._parent.getPLCValue()
        return bool(current & (1 << self._bit))

    def getUAValue(self) -> bool:
        return self.getPLCValue()

    def __bool__(self) -> bool:
        return self.getPLCValue()

    def setValue(self, value: bool):
        current = self._parent.getPLCValue()

        if value:
            current |= 1 << self._bit
        else:
            current &= ~(1 << self._bit)

        self._parent.setValue(current)

    def __repr__(self):
        return repr(self.getPLCValue())

@dataclass(repr=False, eq=False)
class FLOAT_BIT(MEMORY_BIT):
    BYTEORDER = 'little'
    
    _format: str = field(init=False, repr=False, default=None)
    _mask_width: int = field(init=False, repr=False, default=None)
    _bytesize: int = field(init=False, repr=False, default=None)
    
    def __post_init__(self, parent: Type, bit: int) -> None:
        super().__post_init__(parent, bit)
        
        if isinstance(parent, REAL):
            self._format = 'f'         # 32-bit single precision
            self._mask_width = 32
            self._bytesize = 4
        elif isinstance(parent, LREAL):
            self._format = 'd'         # 64-bit double precision
            self._mask_width = 64
            self._bytesize = 8
        else:
            # Fallback for unknown parent types
            raise TypeError(
                f"FLOAT_BIT parent must be REAL or LREAL, got {type(parent).__name__}"
            )
        
        if bit >= self._mask_width:
            raise ValueError(f"bit {bit} out of range [0, {self._mask_width})")
    
    def _to_int(self, value: float) -> int:
        packed = struct.pack(self._format, value)
        return int.from_bytes(packed, byteorder=self.BYTEORDER)
    
    def _int_to_float(self, int_repr: int) -> float:
        packed = int_repr.to_bytes(self._bytesize, byteorder=self.BYTEORDER)
        return struct.unpack(self._format, packed)[0]
    
    def getPLCValue(self) -> bool:
        float_val = self.parent.getPLCValue()
        int_repr = self._to_int(float_val)
        return bool(int_repr & (1 << self._bit))
    
    def setValue(self, value: bool):
        float_val = self.parent.getPLCValue()
        int_repr = self._to_int(float_val)
        
        if value:
            int_repr |= 1 << self._bit
        else:
            int_repr &= ~(1 << self._bit)
        
        new_float = self._int_to_float(int_repr)
        self.parent.setValue(new_float)
    
    def __repr__(self):
        fmt_name = "LREAL" if self._mask_width == 64 else "REAL"
        return f"FLOAT_BIT({fmt_name}, bit={self._bit}, value={self.getPLCValue()})"