from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.array import Array

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_C_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 400))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_128BYTES_I_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_128BYTES_O_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_12BYTES_I_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 3))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_136BYTES_O_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 34))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_168BYTES_I_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 42))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_40BYTES_I_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 10))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_40BYTES_O_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 10))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_DINT_32BYTES_I_0:
    Data: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_32BYTES_I_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_32BYTES_O_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 32))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_34BYTES_I_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 34))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_34BYTES_O_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 34))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_42BYTES_I_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 42))

@DataTypeRegistry.register
@dataclass
class AB_ETHERNET_MODULE_SINT_42BYTES_O_0:
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 42))