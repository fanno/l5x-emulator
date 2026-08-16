from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class SFC_ACTION(UDT):
    Status: DINT = field(init=False, default_factory=DINT)
    A: BOOL = field(init=False, default_factory=BOOL)
    Q: BOOL = field(init=False, default_factory=BOOL)
    PauseTimer: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SFC_STEP(UDT):
    Status: DINT = field(init=False, default_factory=DINT)
    X: BOOL = field(init=False, default_factory=BOOL)
    FS: BOOL = field(init=False, default_factory=BOOL)
    SA: BOOL = field(init=False, default_factory=BOOL)
    LS: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    OV: BOOL = field(init=False, default_factory=BOOL)
    AlarmEn: BOOL = field(init=False, default_factory=BOOL)
    AlarmLow: BOOL = field(init=False, default_factory=BOOL)
    AlarmHigh: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    PauseTimer: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    TMax: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)
    LimitLow: DINT = field(init=False, default_factory=DINT)
    LimitHigh: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SFC_STOP(UDT):
    Status: DINT = field(init=False, default_factory=DINT)
    X: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    Count: DINT = field(init=False, default_factory=DINT)
