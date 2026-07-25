from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_I_0(UDT):
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_O_0(UDT):
    Data: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_DIAG_I_0(UDT):
    Data: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_FT_I_0(UDT):
    Readback: BOOL = field(init=False, default_factory=BOOL)
    Fault: BOOL = field(init=False, default_factory=BOOL)
    Uncertain: BOOL = field(init=False, default_factory=BOOL)
    NoLoad: BOOL = field(init=False, default_factory=BOOL)
    ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    FieldPowerOff: BOOL = field(init=False, default_factory=BOOL)
    ReturnCurrentMismatch: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_FT_O_0(UDT):
    Data: BOOL = field(init=False, default_factory=BOOL)
    ResetFault: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_OVERRIDE_O_0(UDT):
    OverrideDataEn: BOOL = field(init=False, default_factory=BOOL)
    OverrideDataValue: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class CHANNEL_DO_SCHEDULED_O_0(UDT):
    Data: BOOL = field(init=False, default_factory=BOOL)
    ScheduleEn: BOOL = field(init=False, default_factory=BOOL)
