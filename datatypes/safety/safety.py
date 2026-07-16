from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT, REAL, SINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class LIGHT_CURTAIN:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ResetType: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    MuteLightCurtain: BOOL = field(init=False, default_factory=BOOL)
    CircuitReset: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL)
    InputFilterTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    CI: BOOL = field(init=False, default_factory=BOOL)
    CRHO: BOOL = field(init=False, default_factory=BOOL)
    LCB: BOOL = field(init=False, default_factory=BOOL)
    LCM: BOOL = field(init=False, default_factory=BOOL)
    II: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class MUTING_FOUR_SENSOR_BIDIR:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    LightCurtain: BOOL = field(init=False, default_factory=BOOL)
    Sensor1: BOOL = field(init=False, default_factory=BOOL)
    Sensor2: BOOL = field(init=False, default_factory=BOOL)
    Sensor3: BOOL = field(init=False, default_factory=BOOL)
    Sensor4: BOOL = field(init=False, default_factory=BOOL)	
    EnableMute: BOOL = field(init=False, default_factory=BOOL)
    Override: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    MutingLampStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    Direction: BOOL = field(init=False, default_factory=BOOL)
    S1S2Time: DINT = field(init=False, default_factory=DINT)
    S2LCTime: DINT = field(init=False, default_factory=DINT)
    LCS3Time: DINT = field(init=False, default_factory=DINT)
    S3S4Time: DINT = field(init=False, default_factory=DINT)
    MaximumMuteTime: DINT = field(init=False, default_factory=DINT)
    MaximumOverrideTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    ML: BOOL = field(init=False, default_factory=BOOL)
    CA: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class MUTING_TWO_SENSOR_ASYM:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    LightCurtain: BOOL = field(init=False, default_factory=BOOL)
    Sensor1: BOOL = field(init=False, default_factory=BOOL)
    Sensor2: BOOL = field(init=False, default_factory=BOOL)
    Reserved1: BOOL = field(init=False, default_factory=BOOL)
    Reserved2: BOOL = field(init=False, default_factory=BOOL)	
    EnableMute: BOOL = field(init=False, default_factory=BOOL)
    Override: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    MutingLampStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    Direction: BOOL = field(init=False, default_factory=BOOL)
    S1S2Time: DINT = field(init=False, default_factory=DINT)
    S2LCTime: DINT = field(init=False, default_factory=DINT)
    Reserved3: DINT = field(init=False, default_factory=DINT)
    Reserved4: DINT = field(init=False, default_factory=DINT)
    MaximumMuteTime: DINT = field(init=False, default_factory=DINT)
    MaximumOverrideTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    ML: BOOL = field(init=False, default_factory=BOOL)
    CA: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)


@DataTypeRegistry.register
@dataclass
class MUTING_TWO_SENSOR_SYM:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    LightCurtain: BOOL = field(init=False, default_factory=BOOL)
    Sensor1: BOOL = field(init=False, default_factory=BOOL)
    Sensor2: BOOL = field(init=False, default_factory=BOOL)
    Reserved1: BOOL = field(init=False, default_factory=BOOL)
    Reserved2: BOOL = field(init=False, default_factory=BOOL)	
    EnableMute: BOOL = field(init=False, default_factory=BOOL)
    Override: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    MutingLampStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    S1S2DiscrepancyTime: DINT = field(init=False, default_factory=DINT)
    S1S2LCMinimumTime: DINT = field(init=False, default_factory=DINT)
    S1S2LCMaximumTime: DINT = field(init=False, default_factory=DINT)
    Reserved3: DINT = field(init=False, default_factory=DINT)
    MaximumMuteTime: DINT = field(init=False, default_factory=DINT)
    MaximumOverrideTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    ML: BOOL = field(init=False, default_factory=BOOL)
    CA: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class REDUNDANT_INPUT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ResetType: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    CircuitReset: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    CI: BOOL = field(init=False, default_factory=BOOL)
    CRHO: BOOL = field(init=False, default_factory=BOOL)
    II: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class REDUNDANT_OUTPUT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    FeedbackType: BOOL = field(init=False, default_factory=BOOL)
    Enable: BOOL = field(init=False, default_factory=BOOL)
    Feedback1: BOOL = field(init=False, default_factory=BOOL)
    Feedback2: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    O2: BOOL = field(init=False, default_factory=BOOL)
    O1FF: BOOL = field(init=False, default_factory=BOOL)
    O2FF: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class SAFETY_LIMITED_POSITION:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    Request: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    CheckDelayActive: BOOL = field(init=False, default_factory=BOOL)
    CheckDelay: INT = field(init=False, default_factory=INT)
    PositiveTravelLimit: REAL = field(init=False, default_factory=REAL)
    NegativeTravelLimit: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class SAFETY_LIMITED_SPEED:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    Request: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    CheckDelayActive: BOOL = field(init=False, default_factory=BOOL)
    CheckDelay: INT = field(init=False, default_factory=INT)
    ActiveLimit: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class SAFETY_FEEDBACK_INTERFACE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    TimeUnit: BOOL = field(init=False, default_factory=BOOL)
    FeedbackValid: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    HomeTrigger: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    SFH: BOOL = field(init=False, default_factory=BOOL)
    PositionScaling: REAL = field(init=False, default_factory=REAL)
    FeedbackResolution: DINT = field(init=False, default_factory=DINT)
    Unwind: DINT = field(init=False, default_factory=DINT)
    HomePosition: REAL = field(init=False, default_factory=REAL)
    FeedbackPosition: DINT = field(init=False, default_factory=DINT)
    FeedbackVelocity: REAL = field(init=False, default_factory=REAL)
    ActualPosition: REAL = field(init=False, default_factory=REAL)
    ActualCycles: DINT = field(init=False, default_factory=DINT)
    ActualSpeed: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)
    PositionScalingOut: REAL = field(init=False, default_factory=REAL)
    UnwindOut: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SAFETY_MAT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ChannelA: BOOL = field(init=False, default_factory=BOOL)
    ChannelB: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuitDetectDelayTime: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    SRCA: BOOL = field(init=False, default_factory=BOOL)
    SRCB: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    FaultCode: DINT = field(init=False, default_factory=DINT)
    DiagnosticCode: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class SAFE_BREAK_CONTROL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    BrakeFeedback1: BOOL = field(init=False, default_factory=BOOL)
    BrakeFeedback2: BOOL = field(init=False, default_factory=BOOL)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    BrakeEngageL: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    BO1: BOOL = field(init=False, default_factory=BOOL)
    BO2: BOOL = field(init=False, default_factory=BOOL)
    TOR: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    STOtoSBCDelayActive: BOOL = field(init=False, default_factory=BOOL)
    FdbkONChkDlyTimerActive: BOOL = field(init=False, default_factory=BOOL)
    FdbkOFFChkDlyTimerActive: BOOL = field(init=False, default_factory=BOOL)
    STOtoSBCDelay: INT = field(init=False, default_factory=INT)
    BrakeFeedbackCheckDelay: INT = field(init=False, default_factory=INT)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class SAFE_DIRECTION:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    PositiveRequest: BOOL = field(init=False, default_factory=BOOL)
    NegativeRequest: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    PositionWindow: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class SAFE_OPERATING_STOP:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    Request: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    CheckDelayActive: BOOL = field(init=False, default_factory=BOOL)
    Mode: SINT = field(init=False, default_factory=SINT)
    CheckDelay: INT = field(init=False, default_factory=INT)
    StandstillSpeed: REAL = field(init=False, default_factory=REAL)
    StandstillDeadband: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)
    StandStillSetpoint: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SAFE_STOP_1:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    Request: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    StopMonitorDelayActive: BOOL = field(init=False, default_factory=BOOL)
    StopMonitorDelay: INT = field(init=False, default_factory=INT)
    StopDelay: DINT = field(init=False, default_factory=DINT)
    StandstillSpeed: REAL = field(init=False, default_factory=REAL)
    DecelRefSpeed: REAL = field(init=False, default_factory=REAL)
    DecelSpeedTolerance: REAL = field(init=False, default_factory=REAL)
    FaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)
    SpeedLimit: REAL = field(init=False, default_factory=REAL)
    DecelerationRamp: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SAFE_STOP_2:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    RestartType: BOOL = field(init=False, default_factory=BOOL)
    ColdStartType: BOOL = field(init=False, default_factory=BOOL)
    Request: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    O1: BOOL = field(init=False, default_factory=BOOL)
    RR: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
    StopMonitorDelayActive: BOOL = field(init=False, default_factory=BOOL)
    CheckDelayActive: BOOL = field(init=False, default_factory=BOOL)
    StopMonitorDelay: INT = field(init=False, default_factory=INT)
    StopDelay: DINT = field(init=False, default_factory=DINT)
    SS2StandstillSpeed: REAL = field(init=False, default_factory=REAL)
    DecelRefSpeed: REAL = field(init=False, default_factory=REAL)
    DecelSpeedTolerance: REAL = field(init=False, default_factory=REAL)
    Mode: SINT = field(init=False, default_factory=SINT)
    CheckDelay: INT = field(init=False, default_factory=INT)
    SOSStandstillSpeed: REAL = field(init=False, default_factory=REAL)
    StandstillDeadband: REAL = field(init=False, default_factory=REAL)
    SS2FaultType: SINT = field(init=False, default_factory=SINT)
    SOSFaultType: SINT = field(init=False, default_factory=SINT)
    DiagnosticCode: SINT = field(init=False, default_factory=SINT)
    SpeedLimit: REAL = field(init=False, default_factory=REAL)
    DecelerationRamp: REAL = field(init=False, default_factory=REAL)
    StandstillSetpoint: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class TWO_HAND_RUN_STATION:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    ActivePinType: BOOL = field(init=False, default_factory=BOOL)
    ActivePin: BOOL = field(init=False, default_factory=BOOL)
    RightButtonNormallyOpen: BOOL = field(init=False, default_factory=BOOL)
    RightButtonNormallyClosed: BOOL = field(init=False, default_factory=BOOL)
    LeftButtonNormallyOpen: BOOL = field(init=False, default_factory=BOOL)
    LeftButtonNormallyClosed: BOOL = field(init=False, default_factory=BOOL)
    FaultReset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    BP: BOOL = field(init=False, default_factory=BOOL)
    SA: BOOL = field(init=False, default_factory=BOOL)
    BT: BOOL = field(init=False, default_factory=BOOL)
    CB: BOOL = field(init=False, default_factory=BOOL)
    SAF: BOOL = field(init=False, default_factory=BOOL)
    RBF: BOOL = field(init=False, default_factory=BOOL)
    LBF: BOOL = field(init=False, default_factory=BOOL)
    FP: BOOL = field(init=False, default_factory=BOOL)
