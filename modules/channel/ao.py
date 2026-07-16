from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import INT, REAL
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_O_0:
    LLimitAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HLimitAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    RampAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_CAL_O_0:
    LLimitAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HLimitAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    RampAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    Calibrate: BOOL = field(init=False, default_factory=BOOL)
    CalOutputLowRef: BOOL = field(init=False, default_factory=BOOL)
    CalOutputHighRef: BOOL = field(init=False, default_factory=BOOL)
    CalLowRefPassed: BOOL = field(init=False, default_factory=BOOL)
    CalHighRefPassed: BOOL = field(init=False, default_factory=BOOL)
    CalFinished: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)


@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_DIAG_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    OverTemperature: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    InHold: BOOL = field(init=False, default_factory=BOOL)
    NotANumber: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    LLimitAlarm: BOOL = field(init=False, default_factory=BOOL)
    HLimitAlarm: BOOL = field(init=False, default_factory=BOOL)
    RampAlarm: BOOL = field(init=False, default_factory=BOOL)
    CalFault: BOOL = field(init=False, default_factory=BOOL)
    Calibrating: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)
    RollingTimestamp: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_DIAG_CAL_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    OverTemperature: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    InHold: BOOL = field(init=False, default_factory=BOOL)
    NotANumber: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    LLimitAlarm: BOOL = field(init=False, default_factory=BOOL)
    HLimitAlarm: BOOL = field(init=False, default_factory=BOOL)
    RampAlarm: BOOL = field(init=False, default_factory=BOOL)
    CalFault: BOOL = field(init=False, default_factory=BOOL)
    Calibrating: BOOL = field(init=False, default_factory=BOOL)
    CalGoodLowRef: BOOL = field(init=False, default_factory=BOOL)
    CalBadLowRef: BOOL = field(init=False, default_factory=BOOL)
    CalGoodHighRef: BOOL = field(init=False, default_factory=BOOL)
    CalBadHighRef: BOOL = field(init=False, default_factory=BOOL)
    CalSuccessful: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)
    RollingTimestamp: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_FT_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    OverTemperature: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    NotANumber: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)
    RollingTimestamp: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AO_FT_O_0:
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)

