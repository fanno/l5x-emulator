from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class LEAD_LAG(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
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
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    LeadInv: BOOL = field(init=False, default_factory=BOOL)
    LagInv: BOOL = field(init=False, default_factory=BOOL)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class LEAD_LAG_SEC_ORDER(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
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
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    WLeadInv: BOOL = field(init=False, default_factory=BOOL)
    WLagInv: BOOL = field(init=False, default_factory=BOOL)
    ZetaLeadInv: BOOL = field(init=False, default_factory=BOOL)
    ZetaLagInv: BOOL = field(init=False, default_factory=BOOL)
    OrderInv: BOOL = field(init=False, default_factory=BOOL)
    WLagRatioInv: BOOL = field(init=False, default_factory=BOOL)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSTiRTSTimeStampInvmeInv: BOOL = field(init=False, default_factory=BOOL)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL)
