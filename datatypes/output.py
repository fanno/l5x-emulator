from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class OUTPUT_CAM(UDT):
    OutputBit: DINT = field(init=False, default_factory=DINT)
    LatchType: DINT = field(init=False, default_factory=DINT)
    UnlatchType: DINT = field(init=False, default_factory=DINT)
    Left: REAL = field(init=False, default_factory=REAL)
    Right: REAL = field(init=False, default_factory=REAL)
    Duration: REAL = field(init=False, default_factory=REAL)
    EnableType: DINT = field(init=False, default_factory=DINT)
    EnableBit: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class OUTPUT_COMPENSTATION(UDT):
    Offset: REAL = field(init=False, default_factory=REAL)
    LatchDelay: REAL = field(init=False, default_factory=REAL)
    UnlatchDelay: REAL = field(init=False, default_factory=REAL)
    Mode: DINT = field(init=False, default_factory=DINT)
    CycleTime: REAL = field(init=False, default_factory=REAL)
    DutyCycle: REAL = field(init=False, default_factory=REAL)


