from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.array import Array

from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class AB_1734_1Slot_I_0(UDT):
    SlotStatusBits0_31: DINT = field(init=False, default_factory=DINT)
    SlotStatusBits32_63: DINT = field(init=False, default_factory=DINT)
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 1))

@DataTypeRegistry.register
@dataclass
class AB_1734_1Slot_O_0(UDT):
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 1))

@DataTypeRegistry.register
@dataclass
class AB_1734_4Slot_I_0(UDT):
    SlotStatusBits0_31: DINT = field(init=False, default_factory=DINT)
    SlotStatusBits32_63: DINT = field(init=False, default_factory=DINT)
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 4))

@DataTypeRegistry.register
@dataclass
class AB_1734_4Slot_O_0(UDT):
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 4))

@DataTypeRegistry.register
@dataclass
class AB_1734_6Slot_I_0(UDT):
    SlotStatusBits0_31: DINT = field(init=False, default_factory=DINT)
    SlotStatusBits32_63: DINT = field(init=False, default_factory=DINT)
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 6))

@DataTypeRegistry.register
@dataclass
class AB_1734_6Slot_O_0(UDT):
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 6))

@DataTypeRegistry.register
@dataclass
class AB_1734_8Slot_I_0(UDT):
    SlotStatusBits0_31: DINT = field(init=False, default_factory=DINT)
    SlotStatusBits32_63: DINT = field(init=False, default_factory=DINT)
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 8))

@DataTypeRegistry.register
@dataclass
class AB_1734_8Slot_O_0(UDT):
    Data: Array[SINT] = field(init=False, default_factory=lambda: Array.create(SINT, 8))