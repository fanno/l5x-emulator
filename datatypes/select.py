from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class SELECT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    In2: REAL = field(init=False, default_factory=REAL)
    SelectorIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECTABLE_NEGATE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    NegateEnable: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECTED_SUMMER(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    Gain1: REAL = field(init=False, default_factory=REAL)
    Select1: BOOL = field(init=False, default_factory=BOOL)
    In2: REAL = field(init=False, default_factory=REAL)
    Gain2: REAL = field(init=False, default_factory=REAL)
    Select2: BOOL = field(init=False, default_factory=BOOL)
    In3: REAL = field(init=False, default_factory=REAL)
    Gain3: REAL = field(init=False, default_factory=REAL)
    Select3: BOOL = field(init=False, default_factory=BOOL)
    In4: REAL = field(init=False, default_factory=REAL)
    Gain4: REAL = field(init=False, default_factory=REAL)
    Select4: BOOL = field(init=False, default_factory=BOOL)
    In5: REAL = field(init=False, default_factory=REAL)
    Gain5: REAL = field(init=False, default_factory=REAL)
    Select5: BOOL = field(init=False, default_factory=BOOL)
    In6: REAL = field(init=False, default_factory=REAL)
    Gain6: REAL = field(init=False, default_factory=REAL)
    Select6: BOOL = field(init=False, default_factory=BOOL)
    In7: REAL = field(init=False, default_factory=REAL)
    Gain7: REAL = field(init=False, default_factory=REAL)
    Select7: BOOL = field(init=False, default_factory=BOOL)
    In8: REAL = field(init=False, default_factory=REAL)
    Gain8: REAL = field(init=False, default_factory=REAL)
    Select8: BOOL = field(init=False, default_factory=BOOL)
    Bias: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECT_ENHANCED(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    In2: REAL = field(init=False, default_factory=REAL)
    In3: REAL = field(init=False, default_factory=REAL)
    In4: REAL = field(init=False, default_factory=REAL)
    In5: REAL = field(init=False, default_factory=REAL)
    In6: REAL = field(init=False, default_factory=REAL)
    In1Fault: BOOL = field(init=False, default_factory=BOOL)
    In2Fault: BOOL = field(init=False, default_factory=BOOL)
    In3Fault: BOOL = field(init=False, default_factory=BOOL)
    In4Fault: BOOL = field(init=False, default_factory=BOOL)
    In5Fault: BOOL = field(init=False, default_factory=BOOL)
    In6Fault: BOOL = field(init=False, default_factory=BOOL)
    InsUsed: DINT = field(init=False, default_factory=DINT)
    SelectorMode: DINT = field(init=False, default_factory=DINT)
    ProgSelector: DINT = field(init=False, default_factory=DINT)
    OperSelector: DINT = field(init=False, default_factory=DINT)
    ProgProgReq: BOOL = field(init=False, default_factory=BOOL)
    ProgOperReq: BOOL = field(init=False, default_factory=BOOL)
    ProgOverrideReq: BOOL = field(init=False, default_factory=BOOL)
    OperProgReq: BOOL = field(init=False, default_factory=BOOL)
    OperOperReq: BOOL = field(init=False, default_factory=BOOL)
    ProgValueReset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    SelectedIn: DINT = field(init=False, default_factory=DINT)
    ProgOper: BOOL = field(init=False, default_factory=BOOL)
    Override: BOOL = field(init=False, default_factory=BOOL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    InsFaulted: BOOL = field(init=False, default_factory=BOOL)
    InsUsedInv: BOOL = field(init=False, default_factory=BOOL)
    SelectorModeInv: BOOL = field(init=False, default_factory=BOOL)
    ProgSelectorInv: BOOL = field(init=False, default_factory=BOOL)
    OperSelectorInv: BOOL = field(init=False, default_factory=BOOL)