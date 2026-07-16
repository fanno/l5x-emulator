from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import SINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class AB_1734_DO8_NODIAG_C_0:
    FaultMode: SINT = field(init=False, default_factory=SINT)
    Pt0FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt1FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt2FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt3FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt4FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt5FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt6FaultMode: BOOL = field(init=False, default_factory=BOOL)
    Pt7FaultMode: BOOL = field(init=False, default_factory=BOOL)
    FaultValue: SINT = field(init=False, default_factory=SINT)
    Pt0FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt1FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt2FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt3FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt4FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt5FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt6FaultValue: BOOL = field(init=False, default_factory=BOOL)
    Pt7FaultValue: BOOL = field(init=False, default_factory=BOOL)
    ProgMode: SINT = field(init=False, default_factory=SINT)
    Pt0ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt1ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt2ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt3ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt4ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt5ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt6ProgMode: BOOL = field(init=False, default_factory=BOOL)
    Pt7ProgMode: BOOL = field(init=False, default_factory=BOOL)
    ProgValue: SINT = field(init=False, default_factory=SINT)
    Pt0ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt1ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt2ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt3ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt4ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt5ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt6ProgValue: BOOL = field(init=False, default_factory=BOOL)
    Pt7ProgValue: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_1734_OB8S_O_0:
    Pt00Data: BOOL = field(init=False, default_factory=BOOL)
    Pt01Data: BOOL = field(init=False, default_factory=BOOL)
    Pt02Data: BOOL = field(init=False, default_factory=BOOL)
    Pt03Data: BOOL = field(init=False, default_factory=BOOL)
    Pt04Data: BOOL = field(init=False, default_factory=BOOL)
    Pt05Data: BOOL = field(init=False, default_factory=BOOL)
    Pt06Data: BOOL = field(init=False, default_factory=BOOL)
    Pt07Data: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_1734_OB8S_SAFETY1_I_0:
    RunMode: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Pt00OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt01OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt02OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt03OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt04OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt05OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt06OutputStatus: BOOL = field(init=False, default_factory=BOOL)
    Pt07OutputStatus: BOOL = field(init=False, default_factory=BOOL)
