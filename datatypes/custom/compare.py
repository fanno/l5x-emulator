from __future__ import annotations
from dataclasses import dataclass

from typing import Any, TypeVar

T = TypeVar('T')
from datatypes.custom.datavariant import DataVariant

@dataclass(repr=False, eq=False)
class COMPARE():
    def __eq__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.string import STRING
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() == other.getPLCValue()
        elif isinstance(other, STRING):
            return self.getPLCValue() == other.getPLCValue()

        return self.getPLCValue() == other
    
    def __ne__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.string import STRING
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() != other.getPLCValue()
        elif isinstance(other, STRING):
            return self.getPLCValue() != other.getPLCValue()

        return self.getPLCValue() != other    

    def __lt__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() < other.getPLCValue()
        return self.getPLCValue() < other

    def __gt__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() > other.getPLCValue()
        return self.getPLCValue() > other

    def __le__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() <= other.getPLCValue()
        return self.getPLCValue() <= other

    def __ge__(self:DataVariant, other:Any) -> bool:
        from datatypes.custom.numbers import INTIGER, REAL
        if isinstance(other, (INTIGER, REAL)):
            return self.getPLCValue() >= other.getPLCValue()
        return self.getPLCValue() >= other