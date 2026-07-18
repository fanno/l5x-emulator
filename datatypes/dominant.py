from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class DOMINANT_RESET(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Set: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)
    OutNot: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class DOMINANT_SET(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Set: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)
    OutNot: BOOL = field(init=False, default_factory=BOOL)