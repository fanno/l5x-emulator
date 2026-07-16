from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import INT, REAL, USINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)
    RollingTimestamp: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_O_0:
    LLAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    LAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    HAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    HHAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    RateAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    LLAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    LAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HHAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    RateAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    SensorOffset: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_CAL_O_0:
    LLAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    LAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    HAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    HHAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    RateAlarmEn: BOOL = field(init=False, default_factory=BOOL)
    LLAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    LAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    HHAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    RateAlarmUnlatch: BOOL = field(init=False, default_factory=BOOL)
    Calibrate: BOOL = field(init=False, default_factory=BOOL)
    CalLowRef: BOOL = field(init=False, default_factory=BOOL)
    CalHighRef: BOOL = field(init=False, default_factory=BOOL)
    SensorOffset: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_CAL_DIAG_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    Temperature: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_DIAG_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
    OverTemperature: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    NotANumber: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    LLAlarm: BOOL = field(init=False, default_factory=BOOL)
    LAlarm: BOOL = field(init=False, default_factory=BOOL)
    HAlarm: BOOL = field(init=False, default_factory=BOOL)
    HHAlarm: BOOL = field(init=False, default_factory=BOOL)
    RateAlarm: BOOL = field(init=False, default_factory=BOOL)
    CalFault: BOOL = field(init=False, default_factory=BOOL)
    Calibrating: BOOL = field(init=False, default_factory=BOOL)
    Data: REAL = field(init=False, default_factory=REAL)
    RollingTimestamp: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_DIAG_CAL_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
    OverTemperature: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    NotANumber: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    LLAlarm: BOOL = field(init=False, default_factory=BOOL)
    LAlarm: BOOL = field(init=False, default_factory=BOOL)
    HAlarm: BOOL = field(init=False, default_factory=BOOL)
    HHAlarm: BOOL = field(init=False, default_factory=BOOL)
    RateAlarm: BOOL = field(init=False, default_factory=BOOL)
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
class CHANNEL_AI_FT_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
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
class CHANNEL_AI_FT_O_0:
    ResetFault: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_HART_I_0:
    Ch: CHANNEL_AI_I_0 = field(init=False, default_factory=CHANNEL_AI_I_0)
    Class: USINT = field(init=False, default_factory=USINT)
    Unit: USINT = field(init=False, default_factory=USINT)
    Manual: BOOL = field(init=False, default_factory=BOOL)
    Constant: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_NAMMUR_I_0:
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    Underrange: BOOL = field(init=False, default_factory=BOOL)
    Overrange: BOOL = field(init=False, default_factory=BOOL)
    LowSaturation: BOOL = field(init=False, default_factory=BOOL)
    HighSaturation: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_AI_NAMMUR__FT_I_0:
    Ch:CHANNEL_AI_FT_I_0 = field(init=False, default_factory=CHANNEL_AI_FT_I_0)
