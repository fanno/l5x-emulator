from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry
from core.l5k.l5kreader import L5KBOOLBYTEEND, L5KSKIP

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class FBD_BIT_FIELD_DISTRIBUTE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    SourceBit: DINT = field(init=False, default_factory=DINT)
    Length: DINT = field(init=False, default_factory=DINT)
    DestBit: DINT = field(init=False, default_factory=DINT)
    Target: DINT = field(init=False, default_factory=DINT)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_AND(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: BOOL = field(init=False, default_factory=BOOL)
    In2: BOOL = field(init=False, default_factory=BOOL)
    In3: BOOL = field(init=False, default_factory=BOOL)
    In4: BOOL = field(init=False, default_factory=BOOL)
    In5: BOOL = field(init=False, default_factory=BOOL)
    In6: BOOL = field(init=False, default_factory=BOOL)
    In7: BOOL = field(init=False, default_factory=BOOL)
    In8: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_NOT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_OR(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: BOOL = field(init=False, default_factory=BOOL)
    In2: BOOL = field(init=False, default_factory=BOOL)
    In3: BOOL = field(init=False, default_factory=BOOL)
    In4: BOOL = field(init=False, default_factory=BOOL)
    In5: BOOL = field(init=False, default_factory=BOOL)
    In6: BOOL = field(init=False, default_factory=BOOL)
    In7: BOOL = field(init=False, default_factory=BOOL)
    In8: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_XOR(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: BOOL = field(init=False, default_factory=BOOL)
    In2: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_COMPARE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)      
    SourceA: BOOL = field(init=False, default_factory=BOOL)
    SourceB: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_COUNTER(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    CUEnable: BOOL = field(init=False, default_factory=BOOL)
    CDEnable: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    CU: BOOL = field(init=False, default_factory=BOOL)
    CD: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    OV: BOOL = field(init=False, default_factory=BOOL)
    UN: BOOL = field(init=False, default_factory=BOOL)
    ACC: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_LIMIT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)
    LowLimit: REAL = field(init=False, default_factory=REAL)
    Test: REAL = field(init=False, default_factory=REAL)
    HighLimit: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class FBD_LOGICAL(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)    
    SourceA: DINT = field(init=False, default_factory=DINT)
    SourceB: DINT = field(init=False, default_factory=DINT)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_CONVERT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MASK_EQUAL(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    Mask: DINT = field(init=False, default_factory=DINT)
    Target: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MASKED_MOVE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    Mask: DINT = field(init=False, default_factory=DINT)
    Target: DINT = field(init=False, default_factory=DINT)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MASKED_EQUAL(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)
    Source: DINT = field(init=False, default_factory=DINT)
    Mask: DINT = field(init=False, default_factory=DINT)
    Compare: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MATH(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    SourceA: REAL = field(init=False, default_factory=REAL)
    SourceB: REAL = field(init=False, default_factory=REAL)
    Dest: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class FBD_MATH_ADVANCED(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Source: REAL = field(init=False, default_factory=REAL)
    Dest: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class FBD_ONESHOT(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    InputBit: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    OutputBit: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_TIMER(UDT):

    def __post_init__(self):
        self.InstructFault = MEMORY_BIT(self.Status, 0)
        self.PresetInv = MEMORY_BIT(self.Status, 1)

    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    TimerEnable: BOOL = field(init=False, default_factory=BOOL)
    Reset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBOOLBYTEEND)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    EN: BOOL = field(init=False, default_factory=BOOL)
    TT: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    ACC: DINT = field(init=False, default_factory=DINT)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PresetInv: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)

@DataTypeRegistry.register
@dataclass
class FBD_TRUNCATE(UDT):
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Source: REAL = field(init=False, default_factory=REAL)
    Dest: DINT = field(init=False, default_factory=DINT)