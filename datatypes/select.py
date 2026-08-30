from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT, _32BIT_UDT

from core.l5k.l5kreader import L5KSKIP

@DataTypeRegistry.register
@dataclass
class SELECT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    SelectorIn: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    In2: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECTABLE_NEGATE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    NegateEnable: BOOL = field(init=False, default_factory=BOOL)
    In: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECTED_SUMMER(_32BIT_UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Select1: BOOL = field(init=False, default_factory=BOOL)
    Select2: BOOL = field(init=False, default_factory=BOOL)
    Select3: BOOL = field(init=False, default_factory=BOOL)
    Select4: BOOL = field(init=False, default_factory=BOOL)
    Select5: BOOL = field(init=False, default_factory=BOOL)
    Select6: BOOL = field(init=False, default_factory=BOOL)
    Select7: BOOL = field(init=False, default_factory=BOOL)
    Select8: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    Gain1: REAL = field(init=False, default_factory=REAL)
    In2: REAL = field(init=False, default_factory=REAL)
    Gain2: REAL = field(init=False, default_factory=REAL)
    In3: REAL = field(init=False, default_factory=REAL)
    Gain3: REAL = field(init=False, default_factory=REAL)
    In4: REAL = field(init=False, default_factory=REAL)
    Gain4: REAL = field(init=False, default_factory=REAL)
    In5: REAL = field(init=False, default_factory=REAL)
    Gain5: REAL = field(init=False, default_factory=REAL)
    In6: REAL = field(init=False, default_factory=REAL)
    Gain6: REAL = field(init=False, default_factory=REAL)
    In7: REAL = field(init=False, default_factory=REAL)
    Gain7: REAL = field(init=False, default_factory=REAL)
    In8: REAL = field(init=False, default_factory=REAL)
    Gain8: REAL = field(init=False, default_factory=REAL)
    Bias: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class SELECT_ENHANCED(_32BIT_UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.InsFaulted = MEMORY_BIT(self.Status, 1)
        self.InsUsedInv = MEMORY_BIT(self.Status, 2)
        self.SelectorModeInv = MEMORY_BIT(self.Status, 3)
        self.ProgSelectorInv = MEMORY_BIT(self.Status, 4)
        self.OperSelectorInv = MEMORY_BIT(self.Status, 5)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1Fault: BOOL = field(init=False, default_factory=BOOL)
    In2Fault: BOOL = field(init=False, default_factory=BOOL)
    In3Fault: BOOL = field(init=False, default_factory=BOOL)
    In4Fault: BOOL = field(init=False, default_factory=BOOL)
    In5Fault: BOOL = field(init=False, default_factory=BOOL)
    In6Fault: BOOL = field(init=False, default_factory=BOOL)
    ProgOperReq: BOOL = field(init=False, default_factory=BOOL)
    ProgOverrideReq: BOOL = field(init=False, default_factory=BOOL)
    OperProgReq: BOOL = field(init=False, default_factory=BOOL)
    OperOperReq: BOOL = field(init=False, default_factory=BOOL)
    ProgValueReset: BOOL = field(init=False, default_factory=BOOL)
    ProgProgReq: BOOL = field(init=False, default_factory=BOOL)
    In1: REAL = field(init=False, default_factory=REAL)
    In2: REAL = field(init=False, default_factory=REAL)
    In3: REAL = field(init=False, default_factory=REAL)
    In4: REAL = field(init=False, default_factory=REAL)
    In5: REAL = field(init=False, default_factory=REAL)
    In6: REAL = field(init=False, default_factory=REAL)
    InsUsed: DINT = field(init=False, default_factory=DINT)
    SelectorMode: DINT = field(init=False, default_factory=DINT)
    ProgSelector: DINT = field(init=False, default_factory=DINT)
    OperSelector: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    ProgOper: BOOL = field(init=False, default_factory=BOOL)
    Override: BOOL = field(init=False, default_factory=BOOL)
    Out: REAL = field(init=False, default_factory=REAL)
    SelectedIn: DINT = field(init=False, default_factory=DINT)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    InsFaulted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    InsUsedInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    SelectorModeInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ProgSelectorInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    OperSelectorInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)