from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT, LINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_COUNTER_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    Done: BOOL = field(init=False, default_factory=BOOL)
    Rollover: BOOL = field(init=False, default_factory=BOOL)
    Count: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_COUNTER_O_0:
    Reset: BOOL = field(init=False, default_factory=BOOL)
    RolloverAck: BOOL = field(init=False, default_factory=BOOL)
    Preset: DINT = field(init=False, default_factory=DINT)


@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_COUNTER_FT_O_0:
    Reset: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    RolloverAck: BOOL = field(init=False, default_factory=BOOL)
    Preset: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_FT_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    Indeterminate: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_FT_O_0:
    ResetFault: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_TIMESTAMP_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    Chatter: BOOL = field(init=False, default_factory=BOOL)
    TimestampOverflowOffOn: BOOL = field(init=False, default_factory=BOOL)
    TimestampOverflowOnOff: BOOL = field(init=False, default_factory=BOOL)
    CIPSyncValid: BOOL = field(init=False, default_factory=BOOL)
    CIPSyncTimeout: BOOL = field(init=False, default_factory=BOOL)
    TimestampOffOnNumber: INT = field(init=False, default_factory=INT)
    TimestampOnOffNumber: INT = field(init=False, default_factory=INT)
    TimestampOffOn: LINT = field(init=False, default_factory=LINT)
    TimestampOnOff: LINT = field(init=False, default_factory=LINT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_TIMESTAMP_O_0:
    ResetTimestamps: BOOL = field(init=False, default_factory=BOOL)
    TimestampOffOnNumberAck: INT = field(init=False, default_factory=INT)
    TimestampOnOffNumberAck: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_TIMESTAMP_FT_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    OpenWire: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    Chatter: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    Indeterminate: BOOL = field(init=False, default_factory=BOOL)
    TimestampOverflowOffOn: BOOL = field(init=False, default_factory=BOOL)
    TimestampOverflowOnOff: BOOL = field(init=False, default_factory=BOOL)
    CIPSyncValid: BOOL = field(init=False, default_factory=BOOL)
    CIPSyncTimeout: BOOL = field(init=False, default_factory=BOOL)
    TimestampOffOnNumber: INT = field(init=False, default_factory=INT)
    TimestampOnOffNumber: INT = field(init=False, default_factory=INT)
    TimestampOffOn: LINT = field(init=False, default_factory=LINT)
    TimestampOnOff: LINT = field(init=False, default_factory=LINT)
    
@DataTypeRegistry.register
@dataclass
class CHANNEL_DI_TIMESTAMP_FT_O_0:
    ResetFault: BOOL = field(init=False, default_factory=BOOL)
    ResetTimestamps: BOOL = field(init=False, default_factory=BOOL)
    TimestampOffOnNumberAck: INT = field(init=False, default_factory=INT)
    TimestampOnOffNumberAck: INT = field(init=False, default_factory=INT)

