from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import INT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class AB_1734_DI8_C_0:
    Pt0FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt0FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt1FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt1FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt2FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt2FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt3FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt3FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt4FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt4FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt5FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt5FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt6FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt6FilterOnOff: INT = field(init=False, default_factory=INT)
    Pt7FilterOffOn: INT = field(init=False, default_factory=INT)
    Pt7FilterOnOff: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class AB_1734_IB8S_O_0:
    Test00Data: BOOL = field(init=False, default_factory=BOOL)
    Test01Data: BOOL = field(init=False, default_factory=BOOL)
    Test02Data: BOOL = field(init=False, default_factory=BOOL)
    Test03Data: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_1734_IB8S_SAFETY2_O_0:
    RunMode: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Pt00Data: BOOL = field(init=False, default_factory=BOOL)
    Pt01Data: BOOL = field(init=False, default_factory=BOOL)
    Pt02Data: BOOL = field(init=False, default_factory=BOOL)
    Pt03Data: BOOL = field(init=False, default_factory=BOOL)
    Pt04Data: BOOL = field(init=False, default_factory=BOOL)
    Pt05Data: BOOL = field(init=False, default_factory=BOOL)
    Pt06Data: BOOL = field(init=False, default_factory=BOOL)
    Pt07Data: BOOL = field(init=False, default_factory=BOOL)
    Pt00Status: BOOL = field(init=False, default_factory=BOOL)
    Pt01Status: BOOL = field(init=False, default_factory=BOOL)
    Pt02Status: BOOL = field(init=False, default_factory=BOOL)
    Pt03Status: BOOL = field(init=False, default_factory=BOOL)
    Pt04Status: BOOL = field(init=False, default_factory=BOOL)
    Pt05Status: BOOL = field(init=False, default_factory=BOOL)
    Pt06Status: BOOL = field(init=False, default_factory=BOOL)
    Pt07Status: BOOL = field(init=False, default_factory=BOOL)