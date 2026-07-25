from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT,REAL, SINT, USINT
from datatypes.custom.bool import BOOL
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class AB_5000_HART_COMMAND_CONTROL_STRUCT_I_0(UDT):
    ReadyToExecute: BOOL = field(init=False, default_factory=BOOL)
    Completed: BOOL = field(init=False, default_factory=BOOL)
    Active: BOOL = field(init=False, default_factory=BOOL)
    Overlap: BOOL = field(init=False, default_factory=BOOL)
    ERR: BOOL = field(init=False, default_factory=BOOL)
    Warning: BOOL = field(init=False, default_factory=BOOL)
    ParameterError: BOOL = field(init=False, default_factory=BOOL)
    ParameterErrorNumber: SINT = field(init=False, default_factory=SINT)
    ResponseCode: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class AB_5000_HART_COMMAND_CONTROL_STRUCT_O_0(UDT):
    Execute: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_5000_STRING16_STRUCT_I_0(UDT):
    LEN: DINT = field(init=False, default_factory=DINT)
    DATA: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 16))

@DataTypeRegistry.register
@dataclass
class AB_5000_STRING32_STRUCT_I_0(UDT):
    LEN: DINT = field(init=False, default_factory=DINT)
    DATA: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_5000_HART_STATIC_STRUCT_I_0(UDT):
    Fault: BOOL = field(init=False, default_factory=BOOL)
    PVUnit: USINT = field(init=False, default_factory=USINT)
    HARTRevision: USINT = field(init=False, default_factory=USINT)
    HARTTagName: AB_5000_STRING32_STRUCT_I_0 = field(init=False, default_factory=AB_5000_STRING32_STRUCT_I_0)
    Descriptor: AB_5000_STRING16_STRUCT_I_0 = field(init=False, default_factory=AB_5000_STRING16_STRUCT_I_0)
    PVAtSignal4: REAL = field(init=False, default_factory=REAL)
    PVAtSignal20: REAL = field(init=False, default_factory=REAL)
    AdditionalDeviceStatus: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 25))


