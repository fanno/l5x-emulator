from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.string import STRING

from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP, L5KDUMMY

from datatypes.custom.numbers import DINT, REAL, INT, SINT
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT, _32BIT_UDT

@DataTypeRegistry.register
@dataclass
class SEQ_BOOL(UDT):
    Value: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    _lk5_dummy: BOOL = field(init=False, repr=False, default_factory=BOOL, metadata=L5KDUMMY)
    InitialValue: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    Valid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)

@DataTypeRegistry.register
@dataclass
class SEQ_DINT(UDT):
    Value: DINT = field(init=False, default_factory=DINT)
    _lk5_dummy: DINT = field(init=False, repr=False, default_factory=DINT, metadata=L5KDUMMY)
    InitialValue: DINT = field(init=False, default_factory=DINT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_INT(UDT):
    Value: INT = field(init=False, default_factory=INT)
    _lk5_dummy: INT = field(init=False, repr=False, default_factory=INT, metadata=L5KDUMMY)
    InitialValue: INT = field(init=False, default_factory=INT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_REAL(UDT):
    Value: REAL = field(init=False, default_factory=REAL)
    _lk5_dummy: REAL = field(init=False, repr=False, default_factory=REAL, metadata=L5KDUMMY)
    InitialValue: REAL = field(init=False, default_factory=REAL)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_SINT(UDT):
    Value: SINT = field(init=False, default_factory=SINT)
    _lk5_dummy: SINT = field(init=False, repr=False, default_factory=SINT, metadata=L5KDUMMY)
    InitialValue: SINT = field(init=False, default_factory=SINT)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_STEP(_32BIT_UDT):

    def __post_init__(self):
        self.X = MEMORY_BIT(self.Status, 31)
        self.FS = MEMORY_BIT(self.Status, 30)
        self.SA = MEMORY_BIT(self.Status, 0)
        self.LS = MEMORY_BIT(self.Status, 0)
        self.DN = MEMORY_BIT(self.Status, 0)
        self.OV = MEMORY_BIT(self.Status, 0)
        self.AlarmEn = MEMORY_BIT(self.Status, 0)
        self.AlarmLow = MEMORY_BIT(self.Status, 0)
        self.AlarmHigh = MEMORY_BIT(self.Status, 0)
        self.Reset = MEMORY_BIT(self.Status, 0)

        self.Running = MEMORY_BIT(self.State, 0)
        self.Holding = MEMORY_BIT(self.State, 1)
        self.Restarting = MEMORY_BIT(self.State, 2)
        self.Stopping = MEMORY_BIT(self.State, 3)
        self.Aborting = MEMORY_BIT(self.State, 4)
        self.Resetting = MEMORY_BIT(self.State, 5)
        self.Idle = MEMORY_BIT(self.State, 6)
        self.Held = MEMORY_BIT(self.State, 7)
        self.Complete = MEMORY_BIT(self.State, 8)
        self.Stopped = MEMORY_BIT(self.State, 9)
        self.Aborted = MEMORY_BIT(self.State, 10)
        self.Starting = MEMORY_BIT(self.State, 11)
        self.Downloading = MEMORY_BIT(self.State, 13)
        self.NotConnected = MEMORY_BIT(self.State, 14)
        self.Inactive = MEMORY_BIT(self.State, 16)
        self.Unknown = MEMORY_BIT(self.State, 30)

        self.PauseEnabled = MEMORY_BIT(self.PauseControl, 0)
        self.Paused = MEMORY_BIT(self.PauseControl, 1)
        self.AutoPauseEnabled = MEMORY_BIT(self.PauseControl, 2)

        self.StartValid = MEMORY_BIT(self.ValidCommands, 0)
        self.HoldValid = MEMORY_BIT(self.ValidCommands, 1)
        self.StopValid = MEMORY_BIT(self.ValidCommands, 2)
        self.RestartValid = MEMORY_BIT(self.ValidCommands, 3)
        self.AbortValid = MEMORY_BIT(self.ValidCommands, 4)
        self.ResetValid = MEMORY_BIT(self.ValidCommands, 5)
        self.AutoPauseValid = MEMORY_BIT(self.ValidCommands, 8)
        self.PauseValid = MEMORY_BIT(self.ValidCommands, 9)
        self.ResumeValid = MEMORY_BIT(self.ValidCommands, 10)
        self.ClearFailureValid = MEMORY_BIT(self.ValidCommands, 11)

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
    PRE: DINT = field(init=False, default_factory=DINT)
    T: DINT = field(init=False, default_factory=DINT)
    TMax: DINT = field(init=False, default_factory=DINT)
    Count: DINT = field(init=False, default_factory=DINT)
    LimitLow: DINT = field(init=False, default_factory=DINT)
    LimitHigh: DINT = field(init=False, default_factory=DINT)
    State: DINT = field(init=False, default_factory=DINT)
    Running: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Holding: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Restarting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopping: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Aborting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Resetting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Idle: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Held: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Complete: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopped: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Aborted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Starting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Downloading: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    NotConnected: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Inactive: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Unknown: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Mode: DINT = field(init=False, default_factory=DINT)
    Control: DINT = field(init=False, default_factory=DINT)
    PauseControl: DINT = field(init=False, default_factory=DINT)
    PauseEnabled: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Paused: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AutoPauseEnabled: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Index: DINT = field(init=False, default_factory=DINT)
    Failure: DINT = field(init=False, default_factory=DINT)
    InternalFailure: DINT = field(init=False, default_factory=DINT)
    ValidCommands: DINT = field(init=False, default_factory=DINT)
    StartValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    HoldValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    StopValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    RestartValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AbortValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AutoPauseValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PauseValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResumeValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ClearFailureValid: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class SEQ_STRING(UDT):
    Value: STRING = field(init=False, default_factory=STRING)
    _lk5_dummy: STRING = field(init=False, repr=False, default_factory=STRING, metadata=L5KDUMMY)
    InitialValue: STRING = field(init=False, default_factory=STRING)
    Valid: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SEQ_TRANSITION(_32BIT_UDT):

    def __post_init__(self):
        self.Idle = MEMORY_BIT(self.Status, 0)
        self.Arming = MEMORY_BIT(self.Status, 1)
        self.Armed = MEMORY_BIT(self.Status, 2)
        self.Firing = MEMORY_BIT(self.Status, 3)
        self.Stopped = MEMORY_BIT(self.Status, 4)
        self.Aborted = MEMORY_BIT(self.Status, 5)
        self.Held = MEMORY_BIT(self.Status, 6)
        self.Holding = MEMORY_BIT(self.Status, 7)
        self.Unknown = MEMORY_BIT(self.Status, 30)

        self.NotFiring = MEMORY_BIT(self.FiringAttr, 0)
        self.Acquiring = MEMORY_BIT(self.FiringAttr, 1)
        self.Committed = MEMORY_BIT(self.FiringAttr, 3)
        self.Stopping = MEMORY_BIT(self.FiringAttr, 4)
        self.Resetting = MEMORY_BIT(self.FiringAttr, 5)
        self.Paused = MEMORY_BIT(self.FiringAttr, 7)

    Status: BOOL = field(init=False, default_factory=BOOL)
    State: DINT = field(init=False, default_factory=DINT)
    Idle: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Arming: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Armed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Firing: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopped: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Aborted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Held: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Holding: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Unknown: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    FiringAttr: DINT = field(init=False, default_factory=DINT)
    NotFiring: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Acquiring: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Committed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopping: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Resetting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Paused: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)