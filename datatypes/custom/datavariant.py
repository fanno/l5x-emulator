import copy

from dataclasses import dataclass, field
from typing import Any, Self
from asyncua import ua

@dataclass
class DataVariant:
    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Null)
    _py_variant:Any = field(init=False, repr=False, default=None)
    _value:Any = field(init=False, repr=False, default=None)

    def toVariant(self) -> ua.Variant:
        return ua.Variant(Value=self.getUAValue(),
                          VariantType=self._ua_variant)
    
    def fromVariant(self, variant:ua.Variant) -> None:
        if variant.VariantType == self._ua_variant:
            self.setValue(variant.Value)
    
    def setValue(self, value:Any):
        self._value = self.toValue(value)
    
    def getPLCValue(self) -> Any:
        raise NotImplementedError(f"{__class__} getPLCValue not implemented yet")
    
    def getUAValue(self) -> Any:
        raise NotImplementedError(f"{__class__} getUAValue not implemented yet")
    
    @classmethod
    def toValue(self, value:Any) -> Any:
        if value is None:
            default_type = getattr(self, '_py_variant', None)
            if default_type is not None:
                return default_type()
            return None
        else:
            if isinstance(value, DataVariant):
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
