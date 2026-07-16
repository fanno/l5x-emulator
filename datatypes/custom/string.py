from __future__ import annotations
import re

from dataclasses import dataclass, field
from typing import Any, Optional
from asyncua import ua
from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.array import Array
from datatypes.custom.compare import COMPARE

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class STRING(COMPARE, DataVariant):
    _init:Optional[str] = field(init=True, repr=False, default="")
    _maxlength:Optional[int] = field(init=False, repr=False, default=82)

    LEN:DINT = field(init=False, repr=False, default_factory=DINT)
    DATA:Array[SINT] = field(init=False, repr=False, default_factory=lambda: Array.create(SINT, 82))

    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.String)
    _py_variant:Any = field(init=False, repr=False, default=str)

    def __post_init__(self):
        self._maxlength = len(self.DATA)
        self.setValue(self._init)

    def setValue(self, value:str):
        value = self.toValue(value)
        if self._maxlength < len(value):
            value = value[:self._maxlength]

        raw = bytearray(value, 'utf-8')
        length = len(value)

        if length < self._maxlength:
             raw.extend([0] * (self._maxlength - length))

        data:list[int] = []
        for char in raw:
            data.append(char)

        while len(data) < self._maxlength:
            data.append(0)
        
        self.DATA = Array[SINT](SINT, data)
        self.LEN.setValue(length)

    def getUAValue(self) -> str:
        len = self.LEN.getPLCValue()

        if len < 1:
            value = ""
        else:
            if len > self._maxlength:
                len = self._maxlength
            data = self.DATA.getUAValue()
            value = bytes(data[:len]).decode('utf-8')

        
        return value
    
    def getPLCValue(self) -> str:
        return self.getUAValue()
    
    def toString(self) -> str:
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
        
        if isinstance(value, SINT):
            self.DATA[index] = value
        elif isinstance(value, int):
            self.DATA[index].setValue(value)
        else:
            raise TypeError(f"{value}, invalid type")

    def __getitem__(self, i) -> SINT:
        return self.DATA[i]

    def __len__(self) -> int:
        return self.LEN.getPLCValue()

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
    def toValue(self, value:str):
        if value is None:
            value = ""

        value = self.hexToChar(value)
        return value

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