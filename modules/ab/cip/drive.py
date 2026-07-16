from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.bool import BOOL



@DataTypeRegistry.register
@dataclass
class AB_CIP_DRIVE_SAFETY_SI_0:
    ConnectionStatus: DINT = field(init=False, default_factory=DINT)
    RunMode: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Status: SINT = field(init=False, default_factory=SINT)
    TorqueDisabled: BOOL = field(init=False, default_factory=BOOL)
    SafetyFault: BOOL = field(init=False, default_factory=BOOL)
    ResetRequired: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_CIP_DRIVE_SAFETY_SOL_0:
    Command: SINT = field(init=False, default_factory=SINT)
    SafeTorqueOff: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
