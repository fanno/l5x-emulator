from core.registry.datatyperegistry import DataTypeRegistry

from dataclasses import dataclass, field

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP

@DataTypeRegistry.register
@dataclass
class FILTER_HIGH_PASS(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.WLeadInv = MEMORY_BIT(self.Status, 1)
        self.OrderInv = MEMORY_BIT(self.Status, 2)
        self.TimingModeInv = MEMORY_BIT(self.Status, 27)
        self.RTSMissed = MEMORY_BIT(self.Status, 28)
        self.RTSTimeInv = MEMORY_BIT(self.Status, 29)
        self.RTSTimeStampInv = MEMORY_BIT(self.Status, 30)
        self.DeltaTInv = MEMORY_BIT(self.Status, 31)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)    
    In: REAL = field(init=False, default_factory=REAL)
    WLead: REAL = field(init=False, default_factory=REAL)
    Order: DINT = field(init=False, default_factory=DINT)
    TimingMode: DINT = field(init=False, default_factory=DINT)
    OversampleDT: DINT = field(init=False, default_factory=DINT)
    RTSTime: DINT = field(init=False, default_factory=DINT)
    RTSTimeStamp: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    DeltaT: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WLeadInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    OrderInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
	
@DataTypeRegistry.register
@dataclass
class FILTER_LOW_PASS(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.WLagInv = MEMORY_BIT(self.Status, 1)
        self.OrderInv = MEMORY_BIT(self.Status, 2)
        self.TimingModeInv = MEMORY_BIT(self.Status, 27)
        self.RTSMissed = MEMORY_BIT(self.Status, 28)
        self.RTSTimeInv = MEMORY_BIT(self.Status, 29)
        self.RTSTimeStampInv = MEMORY_BIT(self.Status, 30)
        self.DeltaTInv = MEMORY_BIT(self.Status, 31)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    WLag: REAL = field(init=False, default_factory=REAL)
    Order: DINT = field(init=False, default_factory=DINT)
    TimingMode: DINT = field(init=False, default_factory=DINT)
    OversampleDT: DINT = field(init=False, default_factory=DINT)
    RTSTime: DINT = field(init=False, default_factory=DINT)
    RTSTimeStamp: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    DeltaT: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WLagInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    OrderInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class FILTER_NOTCH(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.WNotchInv = MEMORY_BIT(self.Status, 1)
        self.QFactorInv = MEMORY_BIT(self.Status, 2)
        self.OrderInv = MEMORY_BIT(self.Status, 3)
        self.TimingModeInv = MEMORY_BIT(self.Status, 27)
        self.RTSMissed = MEMORY_BIT(self.Status, 28)
        self.RTSTimeInv = MEMORY_BIT(self.Status, 29)
        self.RTSTimeStampInv = MEMORY_BIT(self.Status, 30)
        self.DeltaTInv = MEMORY_BIT(self.Status, 31)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)    
    In: REAL = field(init=False, default_factory=REAL)
    WNotch: REAL = field(init=False, default_factory=REAL)
    QFactor: REAL = field(init=False, default_factory=REAL)
    Order: DINT = field(init=False, default_factory=DINT)
    TimingMode: DINT = field(init=False, default_factory=DINT)
    OversampleDT: DINT = field(init=False, default_factory=DINT)
    RTSTime: DINT = field(init=False, default_factory=DINT)
    RTSTimeStamp: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    DeltaT: REAL = field(init=False, default_factory=REAL)    
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    WNotchInv: BOOL = field(init=False, default_factory=BOOL)
    QFactorInv: BOOL = field(init=False, default_factory=BOOL)
    OrderInv: BOOL = field(init=False, default_factory=BOOL)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL)    
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FIVE_POS_MODE_SELECTOR(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Input1: BOOL = field(init=False, default_factory=BOOL)
    Input2: BOOL = field(init=False, default_factory=BOOL)
    Input3: BOOL = field(init=False, default_factory=BOOL)
    Input4: BOOL = field(init=False, default_factory=BOOL)
    Input5: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    O2: BOOL = field(init=False, default_factory=BOOL)
    O3: BOOL = field(init=False, default_factory=BOOL)
    O4: BOOL = field(init=False, default_factory=BOOL)
    O5: BOOL = field(init=False, default_factory=BOOL)
    NM: BOOL = field(init=False, default_factory=BOOL)
    MMS: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)