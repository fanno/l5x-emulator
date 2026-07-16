from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class MAIN_VALVE_CONTROL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)    
    Actuate: BOOL = field(init=False, default_factory=BOOL)
    FeedbackType: BOOL = field(init=False, default_factory=BOOL)
    Feedback1: BOOL = field(init=False, default_factory=BOOL)
    Feedback2: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    FeedbackReactionTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    O2: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class MANUAL_VALVE_CONTROL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    Keyswitch: BOOL = field(init=False, default_factory=BOOL)
    Bottom: BOOL = field(init=False, default_factory=BOOL)
    FlywheelStopped: BOOL = field(init=False, default_factory=BOOL)
    SafetyEnable: BOOL = field(init=False, default_factory=BOOL)
    Actuate: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class AUX_VALVE_CONTROL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Actuate: BOOL = field(init=False, default_factory=BOOL)
    DelayType: BOOL = field(init=False, default_factory=BOOL)
    OutputFollowsActuate: BOOL = field(init=False, default_factory=BOOL)
    DelayEnable: BOOL = field(init=False, default_factory=BOOL)
    FeedbackType: BOOL = field(init=False, default_factory=BOOL)
    Feedback1: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    DelayTime: DINT = field(init=False, default_factory=DINT)
    FeedbackReactionTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)