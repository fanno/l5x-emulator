from __future__ import annotations
import re

from dataclasses import dataclass, field, InitVar, fields
from typing import Optional, ClassVar, Iterator
from asyncua import ua
from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.array import Array
from datatypes.custom.compare import COMPARE
from datatypes.custom.bool import BOOL, MEMORY_BIT

from core.memory.uimemory import DT
from core.l5k.l5kreader import L5KReader

from protocols.memory import SupportsGetPLCValue
from utils.isplcinstance import isPLCInstance

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class STRING(COMPARE, DataVariant):
    init: InitVar[str] = ""

    _maxlength:Optional[int] = field(init=False, repr=False, default=82)
    _type:ClassVar[DT] = DT.STRING

    LEN:DINT = field(init=False, repr=False, default_factory=DINT)
    DATA:Array[SINT] = field(init=False, repr=False, default_factory=lambda: Array.create(SINT, 82))

    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.String
    _py_variant: ClassVar[type] = str

    def __post_init__(self, init:str):
        self._maxlength = len(self.DATA)
        self.setValue(init)

    def setValue(self, value:str):
        value = self.toValue(value)
        if self._maxlength < len(value):
            value = value[:self._maxlength]

        raw = bytearray(value, 'utf-8')
        length = len(value)
        if length < self._maxlength:
             raw.extend([0] * (self._maxlength - length))

        for idx, char in enumerate(raw):
            if self._maxlength > idx:
                self.DATA[idx].setValue(char)
            else:
                break
        
        self.LEN.setValue(length)

    def _l5k(self, reader:L5KReader):
        for field in fields(self):
            if not field.repr:
                continue

            value = getattr(self, field.name)
            
            if isinstance(value, BOOL):
                value.setValue(reader.nextBool())
            else:
                value.setValue(reader.nextRaw())

    def getUAValue(self) -> str:
        len = self.LEN.getPLCValue()

        if len < 1:
            value = ""
        else:
            if len > self._maxlength:
                len = self._maxlength
            data = self.DATA.getUAValue()
            data = [(b + 256) % 256 for b in data[:len]]
            value = bytes(data[:len]).decode('utf-8')
        return value
    
    def getPLCValue(self) -> str:
        return self.getUAValue()
    
    def toString(self) -> str:
        return self.getPLCValue()

    def __repr__(self):
        return self.getPLCValue()

    '''
    def __setattr__(self, name, value):
        match name:
            case 'DATA':
                self.setValue(value)
            case 'LEN':
                if isinstance (value, DINT):
                    value = value.getPLCValue()

                if value < 0:
                    value = 0
                elif value > self._maxlength:
                    value = self._maxlength

                super().__setattr__(name, DINT(value))
    '''
    
    def __setitem__(self, index: int, value: SINT|int) -> None:
        if not isinstance(index, int):
            raise TypeError(f"{index}, not int")
        if index >= self._maxlength or index < 0:
            raise IndexError(f"{index}, out of range")
        
        if isinstance(value, (SINT|int)):
            self.DATA[index].setValue(value)
        else:
            raise TypeError(f"{value}, invalid type")

    def __getitem__(self, i) -> SINT:
        return self.DATA[i]

    def __len__(self) -> int:
        return self.LEN.getPLCValue()

    def __iter__(self) -> Iterator[SINT]:
        for bit_index in range(len(self)):
            yield self[bit_index]

    def iterbit(self) -> Iterator[MEMORY_BIT]:
        for sint in self:
            for bit in sint:
                yield bit

    @staticmethod
    def chartToHex(text):
        result = []
        for char in text:
            value = ord(char)
            if value < 32 or value == 127:
                result.append(f"${value:02X}")
            else:
                result.append(char)
        return "".join(result)
    
    @staticmethod
    def hexToChar(text):
        def hex_to_char(match):
            return chr(int(match.group(1), 16))
        return re.sub(r'\$([0-9A-F]{2})', hex_to_char, text)
    
    @classmethod
    def toValue(cls, value:str):
        if value is None:
            value = ""
        if isPLCInstance(value, SupportsGetPLCValue):
            value = value.getPLCValue()

        value = cls.hexToChar(value)
        return value

    def fromL5K(self, data):
        length , string = data
        self.setValue(string)
        self.LEN.setValue(length)

@DataTypeRegistry.register
@dataclass
class STRING_32(STRING):
    _maxlength:Optional[int] = field(repr=False, default=32)

    DATA:Array[SINT] = field(init=False, repr=False, default_factory=lambda: Array.create(SINT, 32))

@DataTypeRegistry.register
@dataclass
class STRING_16(STRING):
    _maxlength:Optional[int] = field(repr=False, default=32)

    DATA:Array[SINT] = field(init=False, repr=False, default_factory=lambda: Array.create(SINT, 32))