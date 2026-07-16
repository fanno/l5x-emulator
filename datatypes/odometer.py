from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import INT
from datatypes.custom.array import Array

@DataTypeRegistry.register
@dataclass
class SIGNED_ODOMETER:
    Data: Array[INT] = field(init=False, default_factory=lambda: Array.create(INT, 5))

@DataTypeRegistry.register
@dataclass
class ODOMETER:
    Data: Array[INT] = field(init=False, default_factory=lambda: Array.create(INT, 5))