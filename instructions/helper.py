from typing import Any

from datatypes.custom.numbers import INTIGER
from datatypes.custom.udt import UDT
from engine.fbd.block import FBDBlock

from core.memory.helper import getMemory

from protocols.memory import SupportsGetPLCValue
from utils.isplcinstance import isPLCInstance

def split_to_dint(value: int|SupportsGetPLCValue) -> list[int]:
    if isPLCInstance(value, SupportsGetPLCValue):
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

def getPLCValue(source:Any) -> Any:
    if isPLCInstance(source, SupportsGetPLCValue):
        return source.getPLCValue()
    return source

def isArrayPath(address:str) -> Any:
    return address[-1] == ']'

def splitArrayPath(address:str) -> Any:
    if not isArrayPath(address):
        return (address, [])
    
    key, _, values = address.rpartition("[")
    values = values[:-1]

    dims = []
    for x in values.split(","):
        try:
            dims.append(int(x.strip()))
        except Exception as e:
            dims.append(x.strip())

    return (key, dims)

def getOperand(block:FBDBlock) -> UDT:
    operand:UDT = block.Value
    for name, parm in block.inParams.items():
        if parm.Value is not None:
            if hasattr(operand, name):
                attr = getattr(operand, name)
                attr.setValue(parm.Value)
    return operand

def update_bit(value: int, bit: int, state: bool) -> int:
    if state:
        return value | (1 << bit)
    else:
        return value & ~(1 << bit)