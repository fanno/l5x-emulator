from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Self, Tuple

from datatypes.custom.datavariant import DataVariant

from protocols.memory import SupportsClone, SupportsSetValue, SupportsGetPLCValue

from utils.isplcinstance import isPLCInstance

@dataclass(repr=False)
class MATH():
    # ------------------------------------------------------------------
    # Unary operators
    # ------------------------------------------------------------------
    def __neg__(self:SupportsClone) -> Self:
        return self._clone_with(-self.getPLCValue())

    def __pos__(self:SupportsClone) -> Self:
        return self._clone_with(+self.getPLCValue())

    def __abs__(self:SupportsClone) -> Self:
        return self._clone_with(abs(self.getPLCValue()))

    def __invert__(self:SupportsClone) -> Self:
        return self._clone_with(~self.getPLCValue())

    # ------------------------------------------------------------------
    # Binary arithmetic
    # ------------------------------------------------------------------
    def __add__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() + other)

    def __sub__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() - other)

    def __mul__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() * other)

    def __truediv__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() / other)

    def __floordiv__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() // other)

    def __mod__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(self.getPLCValue() % other)

    def __divmod__(self:SupportsClone, other: Any) -> Tuple[Self, Self]:
        """divmod(obj, other) → (obj // other, obj % other)"""
        return NotImplemented

    def __pow__(self:SupportsClone, other: Any, modulo: DataVariant | None = None) -> Self:
        """obj ** other  (or pow(obj, other, modulo) if modulo is given)"""
        return NotImplemented

    # ------------------------------------------------------------------
    # Reflected (right‑hand) binary operators
    # ------------------------------------------------------------------
    def __radd__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other + self.getPLCValue())

    def __rsub__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other - self.getPLCValue())
    
    def __rmul__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other * self.getPLCValue())

    def __rtruediv__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other / self.getPLCValue())

    def __rfloordiv__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other // self.getPLCValue())

    def __rmod__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other % self.getPLCValue())
    
    def __rpow__(self:SupportsClone, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        return self._clone_with(other ** self.getPLCValue())

    # ------------------------------------------------------------------
    # In‑place (augmented assignment) operators
    # ------------------------------------------------------------------
    def __iadd__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() + other)
        return self

    def __isub__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() - other)
        return self

    def __imul__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() * other)
        return self

    def __itruediv__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() / other)
        return self

    def __ifloordiv__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() // other)
        return self

    def __imod__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()
        
        self.setValue(self.getPLCValue() % other)
        return self

    def __ipow__(self:SupportsSetValue, other: Any, modulo: Any | None = None) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        if modulo is not None:
            if isPLCInstance(modulo, SupportsGetPLCValue):
                modulo = modulo.getPLCValue()
            new_val = pow(self.getPLCValue(), other, modulo)
        else:
            new_val = self.getPLCValue() ** other

        self.setValue(new_val)
        return self

    # ------------------------------------------------------------------
    # Bitwise operators
    # ------------------------------------------------------------------
    def __and__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = self.getPLCValue() & other

        self.setValue(result_val)
        return self

    def __or__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = self.getPLCValue() | other

        self.setValue(result_val)
        return self

    def __xor__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = self.getPLCValue() ^ other

        self.setValue(result_val)
        return self

    def __lshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = self.getPLCValue() << other

        self.setValue(result_val)
        return self

    def __rshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = self.getPLCValue() >> other

        self.setValue(result_val)
        return self

    # ------------------------------------------------------------------
    # Reflected bitwise operators
    # ------------------------------------------------------------------
    def __rand__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = other & self.getPLCValue()

        self.setValue(result_val)
        return self

    def __ror__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = other | self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rxor__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = other ^ self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rlshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = other << self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rrshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        result_val = other >> self.getPLCValue()

        self.setValue(result_val)
        return self

    # ------------------------------------------------------------------
    # In‑place bitwise operators
    # ------------------------------------------------------------------
    def __iand__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        new_val = self.getPLCValue() & other

        self.setValue(new_val)
        return self

    def __ior__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        new_val = self.getPLCValue() | other

        self.setValue(new_val)
        return self

    def __ixor__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        new_val = self.getPLCValue() ^ other

        self.setValue(new_val)
        return self

    def __ilshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        new_val = self.getPLCValue() << other

        self.setValue(new_val)
        return self

    def __irshift__(self:SupportsSetValue, other: Any) -> Self:
        if isPLCInstance(other, SupportsGetPLCValue):
            other = other.getPLCValue()

        new_val = self.getPLCValue() >> other

        self.setValue(new_val)
        return self

    # ------------------------------------------------------------------
    # Miscellaneous numeric‑related dunders
    # ------------------------------------------------------------------
    def __round__(self:SupportsClone, ndigits: int | None = None) -> Self:
        rounded = round(self.getPLCValue(), ndigits)
        return self._clone_with(rounded)