from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class DCAF_INPUT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)    
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: REAL = field(init=False, default_factory=REAL)
    ChannelB: REAL = field(init=False, default_factory=REAL)
    Tolerance: REAL = field(init=False, default_factory=REAL)
    HighLimit: REAL = field(init=False, default_factory=REAL)
    LowLimit: REAL = field(init=False, default_factory=REAL)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    HTP: BOOL = field(init=False, default_factory=BOOL)
    LTP: BOOL = field(init=False, default_factory=BOOL)
    O1OnTime: DINT = field(init=False, default_factory=DINT)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)
    Revision: DINT = field(init=False, default_factory=DINT)


@DataTypeRegistry.register
@dataclass
class DCA_INPUT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)    
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: REAL = field(init=False, default_factory=REAL)
    ChannelB: REAL = field(init=False, default_factory=REAL)
    Tolerance: REAL = field(init=False, default_factory=REAL)
    HighLimit: REAL = field(init=False, default_factory=REAL)
    LowLimit: REAL = field(init=False, default_factory=REAL)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    HTP: BOOL = field(init=False, default_factory=BOOL)
    LTP: BOOL = field(init=False, default_factory=BOOL)
    O1OnTime: DINT = field(init=False, default_factory=DINT)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)
    Revision: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_MONITOR(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    EnablChannelBeIn: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    IS: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_START(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    IS: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_STOP(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    IS: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_STOP_TEST(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    TestRequest: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    IS: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_STOP_TEST_LOCK(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    TestRequest: BOOL = field(init=False, default_factory=BOOL)
    UnlockRequest: BOOL = field(init=False, default_factory=BOOL)
    LockFeedback: BOOL = field(init=False, default_factory=BOOL)
    HazardStopped: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    TC: BOOL = field(init=False, default_factory=BOOL)
    ULC: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class DCI_STOP_TEST_MUTE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    TestRequest: BOOL = field(init=False, default_factory=BOOL)
    Mute: BOOL = field(init=False, default_factory=BOOL)
    MutingLampStatus: BOOL = field(init=False, default_factory=BOOL)
    SafetyFunction: DINT = field(init=False, default_factory=DINT)
    InputType: DINT = field(init=False, default_factory=DINT)
    DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    TestType: DINT = field(init=False, default_factory=DINT)
    TestTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    TC: BOOL = field(init=False, default_factory=BOOL)
    ML: BOOL = field(init=False, default_factory=BOOL)
    SS: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

