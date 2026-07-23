from dataclasses import dataclass, field
from typing import Any

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.compare import COMPARE

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class BOOL(COMPARE, DataVariant):
    _value:bool = field(repr=False, default=False)

    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.Boolean)
    _py_variant:Any = field(init=False, repr=False, default=bool)

    def __post_init__(self):
        self.setValue(self._value)

    def getPLCValue(self) -> bool:
        return self._value
    
    def getUAValue(self) -> bool:
        return self._value
    
    def __bool__(self) -> bool:
        return self._value

    @classmethod
    def toValue(self, value:str|int|bool):
        value = super().toValue(value)
        if isinstance(value, str):
            value = value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(value, int):
            value = value > 0

        if not isinstance(value, bool):
            value = bool(value)
            
        return value
    
@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class BIT(BOOL):
    pass