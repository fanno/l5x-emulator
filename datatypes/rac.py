from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL, INT, LINT
from datatypes.custom.bool import BOOL
from datatypes.custom.array import Array

from datatypes.custom.string import STRING
from datatypes.custom.udt import UDT

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
class RAC_ITF_DVC_PWRDISCRETE_CMD(UDT):
    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    Activate: BOOL = field(init=False, default_factory=BOOL)
    Deactivate: BOOL = field(init=False, default_factory=BOOL)
    CmdDir: BOOL = field(init=False, default_factory=BOOL)
    Jog: BOOL = field(init=False, default_factory=BOOL)
    Fast: BOOL = field(init=False, default_factory=BOOL)
    Slow: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRDISCRETE_SET(UDT):
    InhibitCmd: BOOL = field(init=False, default_factory=BOOL)
    InhibitSet: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRDISCRETE_STS(UDT):
    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    Connected: BOOL = field(init=False, default_factory=BOOL)
    Available: BOOL = field(init=False, default_factory=BOOL)
    Warning: BOOL = field(init=False, default_factory=BOOL)
    Faulted: BOOL = field(init=False, default_factory=BOOL)
    Ready: BOOL = field(init=False, default_factory=BOOL)
    Active: BOOL = field(init=False, default_factory=BOOL)
    CmdDir: BOOL = field(init=False, default_factory=BOOL)
    ActDir: BOOL = field(init=False, default_factory=BOOL)
    CmdSpd: BOOL = field(init=False, default_factory=BOOL)
    Fast: BOOL = field(init=False, default_factory=BOOL)
    Slow: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRMOTION_CMD(UDT):
    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    Activate: BOOL = field(init=False, default_factory=BOOL)
    Deactivate: BOOL = field(init=False, default_factory=BOOL)

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
    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    Connected: BOOL = field(init=False, default_factory=BOOL)
    Available: BOOL = field(init=False, default_factory=BOOL)
    Warning: BOOL = field(init=False, default_factory=BOOL)
    Faulted: BOOL = field(init=False, default_factory=BOOL)
    Ready: BOOL = field(init=False, default_factory=BOOL)
    Active: BOOL = field(init=False, default_factory=BOOL)
    ZeroSpeed: BOOL = field(init=False, default_factory=BOOL)
    NoMotion: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_CMD(UDT):
    bCmd: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    ResetWarn: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    Activate: BOOL = field(init=False, default_factory=BOOL)
    Deactivate: BOOL = field(init=False, default_factory=BOOL)
    CmdDir: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_SET(UDT):
    Speed: REAL = field(init=False, default_factory=REAL)
    InhibitCmd: BOOL = field(init=False, default_factory=BOOL)
    InhibitSet: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class RAC_ITF_DVC_PWRVELOCITY_STS(UDT):
    eState: DINT = field(init=False, default_factory=DINT)
    FirstWarning: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    FirstFault: RAC_EVENT = field(init=False, default_factory=RAC_EVENT)
    eCmdFail: DINT = field(init=False, default_factory=DINT)
    Speed: REAL = field(init=False, default_factory=REAL)
    bSts: INT = field(init=False, default_factory=INT)
    Physical: BOOL = field(init=False, default_factory=BOOL)
    Virtual: BOOL = field(init=False, default_factory=BOOL)
    Connected: BOOL = field(init=False, default_factory=BOOL)
    Available: BOOL = field(init=False, default_factory=BOOL)
    Warning: BOOL = field(init=False, default_factory=BOOL)
    Faulted: BOOL = field(init=False, default_factory=BOOL)
    Ready: BOOL = field(init=False, default_factory=BOOL)
    Active: BOOL = field(init=False, default_factory=BOOL)
    ZeroSpeed: BOOL = field(init=False, default_factory=BOOL)
    ObjCtrl: BOOL = field(init=False, default_factory=BOOL)
    CmdDir: BOOL = field(init=False, default_factory=BOOL)
    ActDir: BOOL = field(init=False, default_factory=BOOL)
    Accelerating: BOOL = field(init=False, default_factory=BOOL)
    Decelerating: BOOL = field(init=False, default_factory=BOOL)
    AtSpeed: BOOL = field(init=False, default_factory=BOOL)