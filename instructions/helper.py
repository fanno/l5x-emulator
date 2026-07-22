from typing import Any, Tuple, List, Union
from datatypes.custom.datavariant import DataVariant

from datatypes.custom.numbers import INTIGER
from datatypes.custom.array import Array

from core.memory.helper import getMemory

def split_to_dint(value: int|DataVariant) -> list[int]:
    if isinstance(value, DataVariant):
        value = value.getPLCValue()

    low_mask = 0xFFFFFFFF

    low = value & low_mask

    high = (value >> 32) & low_mask

    def to_signed_32(x: int) -> int:
        return x if x < 0x80000000 else x - 0x100000000

    low_signed  = to_signed_32(low)
    high_signed = to_signed_32(high)

    return [low_signed, high_signed]

def _maskSize(width: INTIGER) -> int:


    
    return (1 << width) - 1

def _mask(width: int) -> int:
    return (1 << width) - 1

def _AND(a: int, b: int, width: int = 32) -> int:
    return (a & b) & _mask(width)

def _OR(a: int, b: int, width: int = 32) -> int:
    return (a | b) & _mask(width)

def _XOR(a: int, b: int, width: int = 32) -> int:
    return (a ^ b) & _mask(width)

def _NOT(a: int, width: int = 32) -> int:
    return (~a) & _mask(width)

def getPLCValue(source) -> Any:
    if isinstance(source, (DataVariant|Array)):
        return source.getPLCValue()
    return source

def isArrayPath(address) -> Any:
    return address[-1] == ']'

def getRootPath(address) -> Tuple[str, List[Union[int]]]:
    if not isArrayPath(address):
        return address, []
    
    last_bracket_open = address.rfind('[')

    if last_bracket_open == -1:
        return address, []
    
    index = address[last_bracket_open + 1:-1]

    dims = index.split(",")

    for i in range(len(dims)):
        dims[i] = getPLCValue(getMemory(dims[i]))
    
    path = address[:last_bracket_open]
    
    return path, dims