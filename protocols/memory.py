from typing import Any, Self, Protocol, Any, runtime_checkable , TYPE_CHECKING
from asyncua import ua
from lxml.etree import _Element as Element

from core.memory.uimemory import UIMemoryObject

if TYPE_CHECKING:
    from datatypes.custom.bool import BOOL

@runtime_checkable
class SupportsSetValue(Protocol):
    def setValue(self, value: Any) -> None:
        ...

@runtime_checkable
class SupportsGetPLCValue(Protocol):
    def getPLCValue(self) -> Any:
        ...       

@runtime_checkable
class SupportsClone(SupportsGetPLCValue, Protocol):
    def _clone_with(self, new_val: Any) -> Self:
        ...

@runtime_checkable
class SupportsToString(Protocol):
    def toString(self) -> str:
        ...

@runtime_checkable
class SupportsToL5X(Protocol):
    def toL5X(self, element:Element) -> None:
        ...

@runtime_checkable
class SupportsToUi(Protocol):
    def toUI(self, name:str) -> None:
        ...

@runtime_checkable
class SupportsUpdate(Protocol):
    def update(self, new:UIMemoryObject) -> None:
        ...

@runtime_checkable
class isVariant(SupportsGetPLCValue, Protocol):
    #_ua_variant:ua.Variant
    #_py_variant:Any

    def toVariant(self) -> ua.Variant:
        ...

    def fromVariant(self, variant:ua.Variant) -> None:
        ...
    
    def getUAValue(self) -> Any:
        ...


@runtime_checkable
class Resettable(Protocol):
    def _reset(self) -> None: ...

@runtime_checkable
class HasEnable(Protocol):
    EnableIn:"BOOL"
    EnableOut:"BOOL"