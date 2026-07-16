from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from dataclasses import dataclass, field

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class FILTER_HIGH_PASS:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
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
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    WLeadInv: BOOL = field(init=False, default_factory=BOOL)
    OrderInv: BOOL = field(init=False, default_factory=BOOL)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL)    
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL)
	
@DataTypeRegistry.register
@dataclass
class FILTER_LOW_PASS:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
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
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    WLagInv: BOOL = field(init=False, default_factory=BOOL)
    OrderInv: BOOL = field(init=False, default_factory=BOOL)
    TimingModeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSMissed: BOOL = field(init=False, default_factory=BOOL)    
    RTSTimeInv: BOOL = field(init=False, default_factory=BOOL)
    RTSTimeStampInv: BOOL = field(init=False, default_factory=BOOL)
    DeltaTInv: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FILTER_NOTCH:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
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
class FIVE_POS_MODE_SELECTOR:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Input1: BOOL = field(init=False, default_factory=BOOL)
    Input2: BOOL = field(init=False, default_factory=BOOL)
    Input3: BOOL = field(init=False, default_factory=BOOL)
    Input4: BOOL = field(init=False, default_factory=BOOL)
    Input5: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    O2: BOOL = field(init=False, default_factory=BOOL)
    O3: BOOL = field(init=False, default_factory=BOOL)
    O4: BOOL = field(init=False, default_factory=BOOL)
    O5: BOOL = field(init=False, default_factory=BOOL)
    NM: BOOL = field(init=False, default_factory=BOOL)
    MMS: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)

