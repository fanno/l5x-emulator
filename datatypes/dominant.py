from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KBOOLBYTEEND

@DataTypeRegistry.register
@dataclass
class DOMINANT_RESET(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Set: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)
    OutNot: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class DOMINANT_SET(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Set: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)
    OutNot: BOOL = field(init=False, default_factory=BOOL)