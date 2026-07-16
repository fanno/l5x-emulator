from dataclasses import dataclass, field
from asyncua import ua
from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.numbers import DINT, REAL, INT, SINT
from datatypes.custom.bool import BOOL
from datatypes.custom.string import STRING

@DataTypeRegistry.register
@dataclass
class MOTION_GROUP:
    GroupStatus: DINT = field(init=False, default_factory=DINT)
    InhibStatus: BOOL = field(init=False, default_factory=BOOL)
    GroupSynced: BOOL = field(init=False, default_factory=BOOL)
    AxisInhibitStatus: BOOL = field(init=False, default_factory=BOOL)
    AxisTestModeStatus: BOOL = field(init=False, default_factory=BOOL)
    GroupFault: DINT = field(init=False, default_factory=DINT)
    GroupOverlapFault: BOOL = field(init=False, default_factory=BOOL)
    CSTLossFault: BOOL = field(init=False, default_factory=BOOL)
    GroupTaskLoadingFault: BOOL = field(init=False, default_factory=BOOL)
    ClockSyncFault: BOOL = field(init=False, default_factory=BOOL)
    GroupAlarm: DINT = field(init=False, default_factory=DINT)
    ClockSyncAlarm: BOOL = field(init=False, default_factory=BOOL)
    AxisFault: DINT = field(init=False, default_factory=DINT)
    PhysicalAxisFault: BOOL = field(init=False, default_factory=BOOL)
    ModuleFault: BOOL = field(init=False, default_factory=BOOL)
    ConfigFault: BOOL = field(init=False, default_factory=BOOL)
    TaskMaxScanTime: DINT = field(init=False, default_factory=DINT)
    TaskLastScanTime: DINT = field(init=False, default_factory=DINT)
    TaskLastIOTime: DINT = field(init=False, default_factory=DINT)
    TaskMaxIOTime: DINT = field(init=False, default_factory=DINT)
    TaskAverageScanTime: DINT = field(init=False, default_factory=DINT)
    TaskAverageIOTime: DINT = field(init=False, default_factory=DINT)
    AxisFault: DINT = field(init=False, default_factory=DINT)
    AxisFault: DINT = field(init=False, default_factory=DINT)
    AxisFault: DINT = field(init=False, default_factory=DINT)
    AxisFault: DINT = field(init=False, default_factory=DINT)

    '''
    Custom extra tags used for AxisParams to make easy access to be used with (GSV /SSV)
    Could be moved later if need bee
    #unknown  because datatype is unsure
    '''

    CoarseUpdatePeriod: DINT = field(init=False, default_factory=DINT)
    PhaseShift: DINT = field(init=False, default_factory=DINT)
    GeneralFaultType: STRING = field(init=False, default_factory=STRING)
    AutoTagUpdate: STRING = field(init=False, default_factory=STRING)
    Alternate1UpdateMultiplier: DINT = field(init=False, default_factory=DINT)
    Alternate2UpdateMultiplier: DINT = field(init=False, default_factory=DINT)



@DataTypeRegistry.register
@dataclass
class MOTION_INSTRUCTION:
    FLAGS: DINT = field(init=False, default_factory=DINT)
    EN: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    ER: BOOL = field(init=False, default_factory=BOOL)
    PC: BOOL = field(init=False, default_factory=BOOL)
    IP: BOOL = field(init=False, default_factory=BOOL)
    AC: BOOL = field(init=False, default_factory=BOOL)
    ACCEL: BOOL = field(init=False, default_factory=BOOL)
    DECEL: BOOL = field(init=False, default_factory=BOOL)
    TrackingMaster: BOOL = field(init=False, default_factory=BOOL)
    CalculatedDataAvailable: BOOL = field(init=False, default_factory=BOOL)
    ERR: INT = field(init=False, default_factory=BOOL)
    STATUS: SINT = field(init=False, default_factory=SINT)
    STATE: SINT = field(init=False, default_factory=SINT)
    SEGMENT: DINT = field(init=False, default_factory=DINT)
    EXERR: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class MOVING_AVERAGE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    InFault: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
    SampleEnable: BOOL = field(init=False, default_factory=BOOL)
    NumberOfSamples: DINT = field(init=False, default_factory=DINT)
    UseWeights: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    InFaulted: BOOL = field(init=False, default_factory=BOOL)
    NumberOfSampInv: BOOL = field(init=False, default_factory=BOOL)


@DataTypeRegistry.register
@dataclass
class MOVING_STD_DEV:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    InFault: BOOL = field(init=False, default_factory=BOOL)
    Initialize: BOOL = field(init=False, default_factory=BOOL)
    SampleEnable: BOOL = field(init=False, default_factory=BOOL)
    NumberOfSamples: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    Average: REAL = field(init=False, default_factory=REAL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    InFaulted: BOOL = field(init=False, default_factory=BOOL)
    NumberOfSampInv: BOOL = field(init=False, default_factory=BOOL)



