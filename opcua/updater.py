from dataclasses import dataclass, field
from asyncua import ua

from typing import TYPE_CHECKING, Any, Callable, Set, ClassVar

if TYPE_CHECKING:
    from core.signal import Signal
    from core.memory.memory import Memory

@dataclass(eq=False)
class OPCUAUpdater:
    signal:"Signal" = field(init=True)
    memory:"Memory" = field(init=True)
    value:Any = field(init=True)

@dataclass
class OPCUAU:
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.Null
    _py_variant: ClassVar[type[Any] | None] = None

    _opcua_ref:OPCUAUpdater = field(init=False, repr=False, default=None)
    _opcua_updater: Set[OPCUAUpdater] = field(init=False, repr=False, default=None)
    _on_change: Callable[[Any], None] | None = field(init=False,repr=False, default=None)
    _scanCount:int = field(init=False, repr=False, default=-1)

    def toVariant(self) -> ua.Variant:
        return ua.Variant(Value=self.getUAValue(),
                          VariantType=self._ua_variant)

    def fromVariant(self, variant:ua.Variant) -> None:
        if variant.VariantType == self._ua_variant:
            self.setValue(variant.Value)

    def setOPCUAOUdater(self, _opcua_updater:Set[OPCUAUpdater], signal:"Signal", memory:"Memory"):
        self._opcua_ref = OPCUAUpdater(signal, memory, self)
        self._opcua_updater = _opcua_updater
        self._register_change()

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        if self._on_change is None:
            self._on_change = on_change

    def _register_change(self):
        pass

    def _notify_change(self):
        if self._opcua_updater is not None:
            from engine.context import EmulatorContext
            emulator = EmulatorContext.get()
            if emulator:
                if emulator.in_plc_scan:
                    if self._scanCount != emulator.scanCount:
                        self._fire_event(emulator.scanCount)
        elif self._on_change is not None:
            from engine.context import EmulatorContext
            emulator = EmulatorContext.get()
            if emulator:
                if emulator.in_plc_scan:
                    if self._scanCount != emulator.scanCount:
                        self._on_change(emulator.scanCount)
                        self._scanCount = emulator.scanCount

    def _child_changed(self, count:int = None):
        if count is not None:
            if self._scanCount != count:
                if self._on_change is None:
                    self._fire_event(count)
                else:
                    self._on_change(count)
                self._scanCount = count

    def _fire_event(self, count:int ) -> None:
        if self._scanCount != count:
            if self._opcua_updater is not None:
                self._opcua_updater.add(self._opcua_ref)
        self._scanCount = count