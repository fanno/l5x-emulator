from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP

@DataTypeRegistry.register
@dataclass
class LEAD_LAG(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.LeadInv = MEMORY_BIT(self.Status, 1)
        self.LagInv = MEMORY_BIT(self.Status, 2)
        self.TimingModeInv = MEMORY_BIT(self.Status, 27)
        self.RTSMissed = MEMORY_BIT(self.Status, 28)
        self.RTSTimeInv = MEMORY_BIT(self.Status, 29)
        self.RTSTimeStampInv = MEMORY_BIT(self.Status, 30)
        self.DeltaTInv = MEMORY_BIT(self.Status, 31)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)    
    In: REAL = field(init=False, default_factory=REAL)
    Lead: REAL = field(init=False, default_factory=REAL)
    Lag: REAL = field(init=False, default_factory=REAL)
    Gain: REAL = field(init=False, default_factory=REAL)
    Bias: REAL = field(init=False, default_factory=REAL)
    InitialValue: REAL = field(init=False, default_factory=REAL)
    TimingMode: DINT = field(init=False, default_factory=DINT)
    OversampleDT: REAL = field(init=False, default_factory=REAL)
    RTSTime: DINT = field(init=False, default_factory=DINT)
    RTSTimeStamp: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    DeltaT: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    LeadInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    LagInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class LEAD_LAG_SEC_ORDER(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.WLeadInv = MEMORY_BIT(self.Status, 1)
        self.WLagInv = MEMORY_BIT(self.Status, 2)
        self.ZetaLeadInv = MEMORY_BIT(self.Status, 3)
        self.ZetaLagInv = MEMORY_BIT(self.Status, 4)
        self.OrderInv = MEMORY_BIT(self.Status, 5)
        self.WLagRatioInv = MEMORY_BIT(self.Status, 6)
        self.TimingModeInv = MEMORY_BIT(self.Status, 27)
        self.RTSMissed = MEMORY_BIT(self.Status, 28)
        self.RTSTimeInv = MEMORY_BIT(self.Status, 29)
        self.RTSTimeStampInv = MEMORY_BIT(self.Status, 30)
        self.DeltaTInv = MEMORY_BIT(self.Status, 31)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    WLead: REAL = field(init=False, default_factory=REAL)
    WLag: REAL = field(init=False, default_factory=REAL)
    ZetaLead: REAL = field(init=False, default_factory=REAL)
    ZetaLag: REAL = field(init=False, default_factory=REAL)
    Order: DINT = field(init=False, default_factory=DINT)
    TimingMode: DINT = field(init=False, default_factory=DINT)
    OversampleDT: REAL = field(init=False, default_factory=REAL)
    RTSTime: DINT = field(init=False, default_factory=DINT)
    RTSTimeStamp: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    DeltaT: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WLeadInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WLagInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ZetaLeadInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ZetaLagInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    OrderInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WLagRatioInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

