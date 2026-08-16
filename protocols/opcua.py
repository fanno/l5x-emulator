from typing import Any, Protocol, Any, runtime_checkable , TYPE_CHECKING, Set, Callable
from asyncua import ua

if TYPE_CHECKING:
    from core.signal import Signal
    from core.memory.memory import Memory

from opcua.updater import OPCUAUpdater

@runtime_checkable
class SupportsOPCUA(Protocol):
    def setOPCUAOUdater(self, _opcua_updater:Set[OPCUAUpdater], _opcua_ref:tuple["Signal", "Memory"]) -> None:
        ...

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        ...

@runtime_checkable
class SupportsVariant(Protocol):
    def toVariant(self) -> ua.Variant:
        ...

    def fromVariant(self, variant:ua.Variant) -> None:
        ...
    
    def getUAValue(self) -> Any:
        ...
