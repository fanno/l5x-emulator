from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import SINT
from datatypes.custom.bool import BOOL
from datatypes.custom.array import Array

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_SAFETYMODULE_16BYTES_O_0:
    AB_ETHERNET_MODULE_C_0: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 16))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_SAFETYMODULE_20BYTES_I_0:
    RunMode: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 16))