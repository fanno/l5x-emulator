from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class SFC_ACTION:
    LEN: DINT = field(init=False, default_factory=DINT)
    POS: DINT = field(init=False, default_factory=DINT)
    ERROR: DINT = field(init=False, default_factory=DINT)
    EN: BOOL = field(init=False, default_factory=BOOL)
    EU: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    EM: BOOL = field(init=False, default_factory=BOOL)
    ER: BOOL = field(init=False, default_factory=BOOL)
    UL: BOOL = field(init=False, default_factory=BOOL)
    RN: BOOL = field(init=False, default_factory=BOOL)
    FD: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SFC_STEP:
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
class SFC_STOP:
    Status: DINT = field(init=False, default_factory=DINT)
    X: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    Count: DINT = field(init=False, default_factory=DINT)
