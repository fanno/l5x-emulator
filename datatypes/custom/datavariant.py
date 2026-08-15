import copy

from dataclasses import dataclass, field
from typing import Any, Self, Any, ClassVar, TYPE_CHECKING
from asyncua import ua

from  utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryPrimitive, DT

if TYPE_CHECKING:
    from core.signal import Signal
    from core.memory.memory import Memory

from opcua.updater import OPCUAU

@dataclass
class DataVariant(OPCUAU):
    _value:Any = field(init=False, repr=False, default=None)
    _type: ClassVar[DT] = DT.UNKNOWN

    def setValue(self, value:Any):
        old = self._value
        self._value = self.toValue(value)

        if old != self._value:
            self._notify_change()

    def getPLCValue(self) -> Any:
        raise NotImplementedError(f"{__class__} getPLCValue not implemented yet")

    def getUAValue(self) -> Any:
        raise NotImplementedError(f"{__class__} getUAValue not implemented yet")

    def toUI(self, name:str, path_filter: dict[str, dict] | None = None) -> UIMemoryPrimitive:
        return UIMemoryPrimitive(name, Datatype=self._type, Value=self._value)

    @classmethod
    def toValue(cls, value:Any) -> Any:
        if value is None:
            default_type = getattr(cls, '_py_variant', None)
            if default_type is not None:
                return default_type()
            return None
        else:
            from protocols.memory import SupportsGetPLCValue
            if isPLCInstance(value, SupportsGetPLCValue):
                value = value.getPLCValue()
            return value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.getPLCValue()})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.getPLCValue()})"

    def _clone_with(self, new_val: Any) -> Self:
        return self.__class__(new_val)

    def copy(self) -> Self:
        return copy.deepcopy(self)

    def _reset(self) -> Self:
        self.setValue(None)
