from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.string import STRING

from datatypes.custom.numbers import DINT, REAL, INT, SINT
from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class SEQ_BOOL(UDT):
    Value: BOOL = field(init=False, default_factory=BOOL)
    InitialValue: BOOL = field(init=False, default_factory=BOOL)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_DINT(UDT):
    Value: DINT = field(init=False, default_factory=DINT)
    InitialValue: DINT = field(init=False, default_factory=DINT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_INT(UDT):
    Value: INT = field(init=False, default_factory=INT)
    InitialValue: INT = field(init=False, default_factory=INT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_REAL(UDT):
    Value: REAL = field(init=False, default_factory=REAL)
    InitialValue: REAL = field(init=False, default_factory=REAL)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_SINT(UDT):
    Value: SINT = field(init=False, default_factory=SINT)
    InitialValue: SINT = field(init=False, default_factory=SINT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_STEP(UDT):
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
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    TMax: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)
    LimitLow: DINT = field(init=False, default_factory=DINT)
    LimitHigh: DINT = field(init=False, default_factory=DINT)
    State: DINT = field(init=False, default_factory=DINT)
    Running: BOOL = field(init=False, default_factory=BOOL)
    Holding: BOOL = field(init=False, default_factory=BOOL)
    Restarting: BOOL = field(init=False, default_factory=BOOL)
    Stopping: BOOL = field(init=False, default_factory=BOOL)
    Aborting: BOOL = field(init=False, default_factory=BOOL)
    Resetting: BOOL = field(init=False, default_factory=BOOL)
    Idle: BOOL = field(init=False, default_factory=BOOL)
    Held: BOOL = field(init=False, default_factory=BOOL)
    Complete: BOOL = field(init=False, default_factory=BOOL)
    Stopped: BOOL = field(init=False, default_factory=BOOL)
    Aborted: BOOL = field(init=False, default_factory=BOOL)
    Starting: BOOL = field(init=False, default_factory=BOOL)
    Downloading: BOOL = field(init=False, default_factory=BOOL)
    NotConnected: BOOL = field(init=False, default_factory=BOOL)
    Inactive: BOOL = field(init=False, default_factory=BOOL)
    Unknown: BOOL = field(init=False, default_factory=BOOL)
    Mode: DINT = field(init=False, default_factory=DINT)
    Control: DINT = field(init=False, default_factory=DINT)
    PauseControl: DINT = field(init=False, default_factory=DINT)
    PauseEnabled: BOOL = field(init=False, default_factory=BOOL)
    Paused: BOOL = field(init=False, default_factory=BOOL)
    AutoPauseEnabled: BOOL = field(init=False, default_factory=BOOL)
    Index: DINT = field(init=False, default_factory=DINT)
    Failure: DINT = field(init=False, default_factory=DINT)
    InternalFailure: DINT = field(init=False, default_factory=DINT)
    ValidCommands: DINT = field(init=False, default_factory=DINT)
    StartValid: BOOL = field(init=False, default_factory=BOOL)
    HoldValid: BOOL = field(init=False, default_factory=BOOL)
    StopValid: BOOL = field(init=False, default_factory=BOOL)
    RestartValid: BOOL = field(init=False, default_factory=BOOL)
    AbortValid: BOOL = field(init=False, default_factory=BOOL)
    ResetValid: BOOL = field(init=False, default_factory=BOOL)
    AutoPauseValid: BOOL = field(init=False, default_factory=BOOL)
    PauseValid: BOOL = field(init=False, default_factory=BOOL)
    ResumeValid: BOOL = field(init=False, default_factory=BOOL)
    ClearFailureValid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_STRING(UDT):
    Value: STRING = field(init=False, default_factory=STRING)
    InitialValue: STRING = field(init=False, default_factory=STRING)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_TRANSITION(UDT):
    Status: BOOL = field(init=False, default_factory=BOOL)
    State: DINT = field(init=False, default_factory=DINT)
    Idle: BOOL = field(init=False, default_factory=BOOL)
    Arming: BOOL = field(init=False, default_factory=BOOL)
    Armed: BOOL = field(init=False, default_factory=BOOL)
    Firing: BOOL = field(init=False, default_factory=BOOL)
    Stopped: BOOL = field(init=False, default_factory=BOOL)
    Aborted: BOOL = field(init=False, default_factory=BOOL)
    Held: BOOL = field(init=False, default_factory=BOOL)
    Holding: BOOL = field(init=False, default_factory=BOOL)
    Unknown: BOOL = field(init=False, default_factory=BOOL)
    FiringAttr: DINT = field(init=False, default_factory=DINT)
    NotFiring: BOOL = field(init=False, default_factory=BOOL)
    Acquiring: BOOL = field(init=False, default_factory=BOOL)
    Committed: BOOL = field(init=False, default_factory=BOOL)
    Stopping: BOOL = field(init=False, default_factory=BOOL)
    Resetting: BOOL = field(init=False, default_factory=BOOL)
    Paused: BOOL = field(init=False, default_factory=BOOL)
