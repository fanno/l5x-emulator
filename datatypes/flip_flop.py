from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class FLIP_FLOP_D:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    D: BOOL = field(init=False, default_factory=BOOL)
    Clear: BOOL = field(init=False, default_factory=BOOL)
    Clock: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Q: BOOL = field(init=False, default_factory=BOOL)
    QNot: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FLIP_FLOP_JK:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Clear: BOOL = field(init=False, default_factory=BOOL)
    Clock: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Q: BOOL = field(init=False, default_factory=BOOL)
    QNot: BOOL = field(init=False, default_factory=BOOL)