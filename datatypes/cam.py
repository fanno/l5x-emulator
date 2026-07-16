from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL, LREAL
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CAM:
    Master: REAL = field(init=False, default_factory=REAL)
    Slave: REAL = field(init=False, default_factory=REAL)
    SegmentType: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CAMSHAFT_MONITOR:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    MotionRequest: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    MechanicalDelayTime: DINT = field(init=False, default_factory=DINT)
    MaxPulsePeriod: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    MeasuredStartTime: DINT = field(init=False, default_factory=DINT)
    MeasuredStopTime: DINT = field(init=False, default_factory=DINT)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CAMS_EXTENDED:
    Master: LREAL = field(init=False, default_factory=LREAL)
    Slave: LREAL = field(init=False, default_factory=LREAL)    
    SegmentType: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CAMS_PROFILE:
    Status: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CAMS_PROFILE_EXTENDED:
    Status: DINT = field(init=False, default_factory=DINT)
    SegmentType: DINT = field(init=False, default_factory=DINT)
    Master: LREAL = field(init=False, default_factory=LREAL)
    Slave: LREAL = field(init=False, default_factory=LREAL)
    C0: LREAL = field(init=False, default_factory=LREAL)
    C1: LREAL = field(init=False, default_factory=LREAL)
    C2: LREAL = field(init=False, default_factory=LREAL)
    C3: LREAL = field(init=False, default_factory=LREAL)