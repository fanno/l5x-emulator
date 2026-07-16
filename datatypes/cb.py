from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CB_CONTINUOUS_MODE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    AckType: BOOL = field(init=False, default_factory=BOOL)
    TakeoverMode: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnable: BOOL = field(init=False, default_factory=BOOL)
    StandardEnable: BOOL = field(init=False, default_factory=BOOL)
    ArmContinuous: BOOL = field(init=False, default_factory=BOOL)
    Start: BOOL = field(init=False, default_factory=BOOL)
    StopAtTop: BOOL = field(init=False, default_factory=BOOL)
    PressInMotion: BOOL = field(init=False, default_factory=BOOL)
    MotionMonitorFault: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnableAck: BOOL = field(init=False, default_factory=BOOL)
    Mode: DINT = field(init=False, default_factory=DINT)    
    SlideZone: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    CA: BOOL = field(init=False, default_factory=BOOL)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CB_CRANKSHAFT_POS_MONITOR:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    CamProfile: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    BrakeCam: BOOL = field(init=False, default_factory=BOOL)
    TakeoverCam: BOOL = field(init=False, default_factory=BOOL)
    DynamicCam: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reverse: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    PressMotionStatus: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    TZ: BOOL = field(init=False, default_factory=BOOL)
    DZ: BOOL = field(init=False, default_factory=BOOL)
    UZ: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    SlideZone: DINT = field(init=False, default_factory=DINT)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CB_INCH_MODE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    AckType: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnable: BOOL = field(init=False, default_factory=BOOL)
    StandardEnable: BOOL = field(init=False, default_factory=BOOL)
    Start: BOOL = field(init=False, default_factory=BOOL)
    PressInMotion: BOOL = field(init=False, default_factory=BOOL)
    MotionMonitorFault: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnableAck: BOOL = field(init=False, default_factory=BOOL)
    SlideZone: DINT = field(init=False, default_factory=DINT)
    InchTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CB_SINGLE_STROKE_MODE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    AckType: BOOL = field(init=False, default_factory=BOOL)
    TakeoverMode: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnable: BOOL = field(init=False, default_factory=BOOL)
    StandardEnable: BOOL = field(init=False, default_factory=BOOL)
    Start: BOOL = field(init=False, default_factory=BOOL)
    PressInMotion: BOOL = field(init=False, default_factory=BOOL)
    MotionMonitorFault: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnableAck: BOOL = field(init=False, default_factory=BOOL)
    SlideZone: DINT = field(init=False, default_factory=DINT)
    InchTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)
