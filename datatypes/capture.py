from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import REAL
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class MAXIMUM_CAPTURE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    ResetValue: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class MINIMUM_CAPTURE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    ResetValue: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)