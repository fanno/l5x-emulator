from __future__ import annotations
from dataclasses import dataclass

from typing import Any, TypeVar

T = TypeVar('T')

import protocols.memory

from utils.isplcinstance import isPLCInstance

@dataclass(repr=False, eq=False)
class COMPARE():
    def __eq__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() == other
    
    def __ne__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() != other    

    def __lt__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() < other

    def __gt__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() > other

    def __le__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() <= other

    def __ge__(self:protocols.memory.SupportsGetPLCValue, other:Any) -> bool:
        if isPLCInstance(other, protocols.memory.SupportsGetPLCValue):
            other = other.getPLCValue()

        return self.getPLCValue() >= other