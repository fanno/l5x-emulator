from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KSKIP

@DataTypeRegistry.register
@dataclass
class SFC_ACTION(UDT):

    def __post_init__(self):
        self.A = MEMORY_BIT(self.Status, 31)
        self.Q = MEMORY_BIT(self.Status, 30)
        self.PauseTimer = MEMORY_BIT(self.Status, 21)

    Status: DINT = field(init=False, default_factory=DINT)
    A: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Q: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PauseTimer: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SFC_STEP(UDT):

    def __post_init__(self):
        self.X = MEMORY_BIT(self.Status, 31)
        self.FS = MEMORY_BIT(self.Status, 30)
        self.SA = MEMORY_BIT(self.Status, 29)
        self.LS = MEMORY_BIT(self.Status, 28)
        self.DN = MEMORY_BIT(self.Status, 27)
        self.OV = MEMORY_BIT(self.Status, 26)
        self.AlarmEn = MEMORY_BIT(self.Status, 25)
        self.AlarmLow = MEMORY_BIT(self.Status, 24)
        self.AlarmHigh = MEMORY_BIT(self.Status, 23)
        self.Reset = MEMORY_BIT(self.Status, 22)
        self.PauseTimer = MEMORY_BIT(self.Status, 21)

    Status: DINT = field(init=False, default_factory=DINT)
    X: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    FS: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    SA: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    LS: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DN: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    OV: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AlarmEn: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AlarmLow: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AlarmHigh: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Reset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PauseTimer: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    TMax: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)
    LimitLow: DINT = field(init=False, default_factory=DINT)
    LimitHigh: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SFC_STOP(UDT):
    def __post_init__(self):
        self.X = MEMORY_BIT(self.Status, 31)
        self.Reset = MEMORY_BIT(self.Status, 22)

    Status: DINT = field(init=False, default_factory=DINT)
    X: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Reset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Count: DINT = field(init=False, default_factory=DINT)
