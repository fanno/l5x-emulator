from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_O_0:
    Data: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_DIAG_I_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_FT_I_0:
    Readback: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    ReturnCurrentMismatch: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_FT_O_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_OVERRIDE_O_0:
    OverrideDataEn: BOOL = field(init=False, default_factory=BOOL)
    OverrideDataValue: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_SCHEDULED_O_0:
    Data: BOOL = field(init=False, default_factory=BOOL)
    ScheduleEn: BOOL = field(init=False, default_factory=BOOL)
