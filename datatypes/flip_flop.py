from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP

@DataTypeRegistry.register
@dataclass
class FLIP_FLOP_D(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    D: BOOL = field(init=False, default_factory=BOOL)
    Clear: BOOL = field(init=False, default_factory=BOOL)
    Clock: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Q: BOOL = field(init=False, default_factory=BOOL)
    QNot: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FLIP_FLOP_JK(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Clear: BOOL = field(init=False, default_factory=BOOL)
    Clock: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Q: BOOL = field(init=False, default_factory=BOOL)
    QNot: BOOL = field(init=False, default_factory=BOOL)