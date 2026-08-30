from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL, INT, LINT
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.array import Array

from datatypes.custom.string import STRING
from datatypes.custom.udt import UDT, _32BIT_UDT

from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP

@DataTypeRegistry.register
@dataclass
class RAC_CODE_DESCRIPTION(UDT):
    Code: DINT = field(init=False, default_factory=DINT)
    Desc: STRING = field(init=False, default_factory=STRING)

@DataTypeRegistry.register
@dataclass
class RAC_EVENT(UDT):
    Type: DINT = field(init=False, default_factory=DINT)
    ID: DINT = field(init=False, default_factory=DINT)
    Category: DINT = field(init=False, default_factory=DINT)
    Action: DINT = field(init=False, default_factory=DINT)
    Value: DINT = field(init=False, default_factory=DINT)
    Message: STRING = field(init=False, default_factory=STRING)
    EventTime_L: LINT = field(init=False, default_factory=LINT)
    EventTime_D: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 7))

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRDISCRETE_CMD(_32BIT_UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.bCmd, 0)
        self.Virtual = MEMORY_BIT(self.bCmd, 1)
        self.ResetWarn = MEMORY_BIT(self.bCmd, 2)
        self.ResetFault = MEMORY_BIT(self.bCmd, 3)
        self.Activate = MEMORY_BIT(self.bCmd, 4)
        self.Deactivate = MEMORY_BIT(self.bCmd, 5)
        self.CmdDir = MEMORY_BIT(self.bCmd, 6)
        self.Jog = MEMORY_BIT(self.bCmd, 7)
        self.Fast = MEMORY_BIT(self.bCmd, 8)
        self.Slow = MEMORY_BIT(self.bCmd, 9)

    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Activate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Deactivate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CmdDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Jog: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Fast: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Slow: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRDISCRETE_SET(UDT):
    InhibitCmd: BOOL = field(init=False, default_factory=BOOL)
    InhibitSet: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRDISCRETE_STS(_32BIT_UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.bSts, 0)
        self.Virtual = MEMORY_BIT(self.bSts, 1)
        self.Connected = MEMORY_BIT(self.bSts, 2)
        self.Available = MEMORY_BIT(self.bSts, 3)
        self.Warning = MEMORY_BIT(self.bSts, 4)
        self.Faulted = MEMORY_BIT(self.bSts, 5)
        self.Ready = MEMORY_BIT(self.bSts, 6)
        self.Active = MEMORY_BIT(self.bSts, 7)
        self.CmdDir = MEMORY_BIT(self.bSts, 8)
        self.ActDir = MEMORY_BIT(self.bSts, 9)
        self.CmdSpd = MEMORY_BIT(self.bSts, 10)
        self.Fast = MEMORY_BIT(self.bSts, 11)
        self.Slow = MEMORY_BIT(self.bSts, 12)

    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Connected: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Available: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Warning: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Faulted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Ready: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Active: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CmdDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ActDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CmdSpd: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Fast: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Slow: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRMOTION_CMD(_32BIT_UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.bCmd, 2)
        self.Virtual = MEMORY_BIT(self.bCmd, 3)
        self.ResetWarn = MEMORY_BIT(self.bCmd, 0)
        self.ResetFault = MEMORY_BIT(self.bCmd, 1)
        self.Activate = MEMORY_BIT(self.bCmd, 4)
        self.Deactivate = MEMORY_BIT(self.bCmd, 5)

    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Activate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Deactivate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRMOTION_INF(UDT):
    AxisID: DINT = field(init=False, default_factory=DINT)
    Lock: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRMOTION_SET(UDT):
    InhibitCmd: BOOL = field(init=False, default_factory=BOOL)
    InhibitSet: BOOL = field(init=False, default_factory=BOOL)
    Lock: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRMOTION_STS(UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.eState, 4)
        self.Virtual = MEMORY_BIT(self.eState, 5)
        self.Connected = MEMORY_BIT(self.eState, 0)
        self.Available = MEMORY_BIT(self.eState, 1)
        self.Warning = MEMORY_BIT(self.eState, 2)
        self.Faulted = MEMORY_BIT(self.eState, 3)
        self.Ready = MEMORY_BIT(self.eState, 4)
        self.Active = MEMORY_BIT(self.eState, 5)
        self.ZeroSpeed = MEMORY_BIT(self.eState, 7)
        self.NoMotion = MEMORY_BIT(self.eState, 6)

    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Connected: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Available: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Warning: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Faulted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Ready: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Active: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ZeroSpeed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    NoMotion: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_CMD(UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.bCmd, 0)
        self.Virtual = MEMORY_BIT(self.bCmd, 1)
        self.ResetWarn = MEMORY_BIT(self.bCmd, 2)
        self.ResetFault = MEMORY_BIT(self.bCmd, 3)
        self.Activate = MEMORY_BIT(self.bCmd, 4)
        self.Deactivate = MEMORY_BIT(self.bCmd, 5)
        self.CmdDir = MEMORY_BIT(self.bCmd, 6)

    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ResetFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Activate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Deactivate: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CmdDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_SET(UDT):
    InhibitCmd: BOOL = field(init=False, default_factory=BOOL)
    InhibitSet: BOOL = field(init=False, default_factory=BOOL)    
    Speed: REAL = field(init=False, default_factory=REAL)


@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_STS(_32BIT_UDT):

    def __post_init__(self):
        self.Physical = MEMORY_BIT(self.bSts, 0)
        self.Virtual = MEMORY_BIT(self.bSts, 1)
        self.Connected = MEMORY_BIT(self.bSts, 2)
        self.Available = MEMORY_BIT(self.bSts, 3)
        self.Warning = MEMORY_BIT(self.bSts, 4)
        self.Faulted = MEMORY_BIT(self.bSts, 5)
        self.Ready = MEMORY_BIT(self.bSts, 6)
        self.Active = MEMORY_BIT(self.bSts, 7)
        self.ZeroSpeed = MEMORY_BIT(self.bSts, 8)
        self.ObjCtrl = MEMORY_BIT(self.bSts, 9)
        self.CmdDir = MEMORY_BIT(self.bSts, 10)
        self.ActDir = MEMORY_BIT(self.bSts, 11)
        self.Accelerating = MEMORY_BIT(self.bSts, 12)
        self.Decelerating = MEMORY_BIT(self.bSts, 13)
        self.AtSpeed = MEMORY_BIT(self.bSts, 14)

    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    Speed: REAL = field(init=False, default_factory=REAL)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Virtual: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Connected: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Available: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Warning: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Faulted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Ready: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Active: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ZeroSpeed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ObjCtrl: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CmdDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ActDir: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Accelerating: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Decelerating: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AtSpeed: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)