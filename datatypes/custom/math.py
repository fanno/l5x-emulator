from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Self, Tuple

from datatypes.custom.datavariant import DataVariant

@dataclass(repr=False)
class MATH():
    # ------------------------------------------------------------------
    # Unary operators
    # ------------------------------------------------------------------
    def __neg__(self:DataVariant) -> Self:
        return self._clone_with(-self.getPLCValue())

    def __pos__(self:DataVariant) -> Self:
        return self._clone_with(+self.getPLCValue())

    def __abs__(self:DataVariant) -> Self:
        return self._clone_with(abs(self.getPLCValue()))

    def __invert__(self:DataVariant) -> Self:
        return self._clone_with(~self.getPLCValue())   

    # ------------------------------------------------------------------
    # Binary arithmetic
    # ------------------------------------------------------------------
    def __add__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() + value)

    def __sub__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() - value)

    def __mul__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() * value)

    def __truediv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() / value)

    def __floordiv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() // value)

    def __mod__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(self.getPLCValue() % value)

    def __divmod__(self:DataVariant, other: Any) -> Tuple[Self, Self]:
        """divmod(obj, other) → (obj // other, obj % other)"""
        return NotImplemented

    def __pow__(self:DataVariant,
                other: Any,
                modulo: DataVariant | None = None) -> Self:
        """obj ** other  (or pow(obj, other, modulo) if modulo is given)"""
        return NotImplemented

    # ------------------------------------------------------------------
    # Reflected (right‑hand) binary operators
    # ------------------------------------------------------------------
    def __radd__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value + self.getPLCValue())

    def __rsub__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value - self.getPLCValue())
    
    def __rmul__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value * self.getPLCValue())

    def __rtruediv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value / self.getPLCValue())

    def __rfloordiv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value // self.getPLCValue())

    def __rmod__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value % self.getPLCValue())
    
    def __rpow__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other

        return self._clone_with(value ** self.getPLCValue())

    # ------------------------------------------------------------------
    # In‑place (augmented assignment) operators
    # ------------------------------------------------------------------
    def __iadd__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() + value)
        return self

    def __isub__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() - value)
        return self

    def __imul__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() * value)
        return self

    def __itruediv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() / value)
        return self

    def __ifloordiv__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() // value)
        return self

    def __imod__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            value = other.getPLCValue()
        elif isinstance(other, (int, float)):
            value = other
        
        self.setValue(self.getPLCValue() % value)
        return self

    def __ipow__(self:DataVariant, other: Any, modulo: DataVariant | None = None) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            exp = other.getPLCValue()
        elif isinstance(other, (int, float)):
            exp = other

        if modulo is not None:
            if isinstance(other, (INTIGER, REAL, DT)):
                mod = modulo.getPLCValue()
            elif isinstance(modulo, (int, float)):
                mod = modulo
            new_val = pow(self.getPLCValue(), exp, mod)
        else:
            new_val = self.getPLCValue() ** exp

        self.setValue(new_val)
        return self

    # ------------------------------------------------------------------
    # Bitwise operators
    # ------------------------------------------------------------------
    def __and__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = self.getPLCValue() & other_val

        self.setValue(result_val)
        return self

    def __or__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = self.getPLCValue() | other_val

        self.setValue(result_val)
        return self

    def __xor__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = self.getPLCValue() ^ other_val

        self.setValue(result_val)
        return self

    def __lshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = self.getPLCValue() << other_val

        self.setValue(result_val)
        return self

    def __rshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = self.getPLCValue() >> other_val

        self.setValue(result_val)
        return self

    # ------------------------------------------------------------------
    # Reflected bitwise operators
    # ------------------------------------------------------------------
    def __rand__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = other_val & self.getPLCValue()

        self.setValue(result_val)
        return self

    def __ror__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = other_val | self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rxor__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = other_val ^ self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rlshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = other_val << self.getPLCValue()

        self.setValue(result_val)
        return self

    def __rrshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other

        result_val = other_val >> self.getPLCValue()

        self.setValue(result_val)
        return self

    # ------------------------------------------------------------------
    # In‑place bitwise operators
    # ------------------------------------------------------------------
    def __iand__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other
        else:
            return NotImplemented

        new_val = self.getPLCValue() & other_val

        self.setValue(new_val)
        return self

    def __ior__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other
        else:
            return NotImplemented

        new_val = self.getPLCValue() | other_val

        self.setValue(new_val)
        return self

    def __ixor__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other
        else:
            return NotImplemented

        new_val = self.getPLCValue() ^ other_val

        self.setValue(new_val)
        return self

    def __ilshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other
        else:
            return NotImplemented

        new_val = self.getPLCValue() << other_val

        self.setValue(new_val)
        return self

    def __irshift__(self:DataVariant, other: Any) -> Self:
        from datatypes.custom.numbers import INTIGER, REAL
        from datatypes.custom.dt import DT

        if isinstance(other, (INTIGER, REAL, DT)):
            other_val = other.getPLCValue()
        elif isinstance(other, int):
            other_val = other
        else:
            return NotImplemented

        new_val = self.getPLCValue() >> other_val

        self.setValue(new_val)
        return self

    # ------------------------------------------------------------------
    # Miscellaneous numeric‑related dunders
    # ------------------------------------------------------------------
    def __round__(self:DataVariant, ndigits: int | None = None) -> Self:
        rounded = round(self.getPLCValue(), ndigits)
        return self._clone_with(rounded)