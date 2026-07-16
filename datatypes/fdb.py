from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, REAL
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class FBD_BIT_DIELD_DISTRIBUTE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    SourceBit: DINT = field(init=False, default_factory=DINT)
    Length: DINT = field(init=False, default_factory=DINT)
    DestBit: DINT = field(init=False, default_factory=DINT)
    Target: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_AND:
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
class FBD_NOT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_OR:
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
class FBD_BOOLEAN_XOR:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    In1: BOOL = field(init=False, default_factory=BOOL)
    In2: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_COMPARE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    SourceA: BOOL = field(init=False, default_factory=BOOL)
    SourceB: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)        

@DataTypeRegistry.register
@dataclass
class FBD_BOOLEAN_CONVERT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_COUNTER:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    CUEnable: BOOL = field(init=False, default_factory=BOOL)
    CDEnable: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    ACC: DINT = field(init=False, default_factory=DINT)
    CU: BOOL = field(init=False, default_factory=BOOL)
    CD: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    OV: BOOL = field(init=False, default_factory=BOOL)
    UN: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_LIMIT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    LowLimit: REAL = field(init=False, default_factory=REAL)
    Test: REAL = field(init=False, default_factory=REAL)
    HighLimit: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Out: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_LOGICAL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    SourceA: DINT = field(init=False, default_factory=DINT)
    SourceB: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)
    
@DataTypeRegistry.register
@dataclass
class FBD_MASKED_MOVE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    Mask: DINT = field(init=False, default_factory=DINT)
    Target: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MASKED_EQUAL:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: DINT = field(init=False, default_factory=DINT)
    Mask: DINT = field(init=False, default_factory=DINT)
    Compare: DINT = field(init=False, default_factory=DINT)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)

@DataTypeRegistry.register
@dataclass
class FBD_MATH:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    SourceA: REAL = field(init=False, default_factory=REAL)
    SourceB: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class FBD_MATH_ADVANCED:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: REAL = field(init=False, default_factory=REAL)

@DataTypeRegistry.register
@dataclass
class FBD_ONESHOT:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    InputBit: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    OutputBit: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_TIMER:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    TimerEnable: BOOL = field(init=False, default_factory=BOOL)
    PRE: DINT = field(init=False, default_factory=DINT)
    Reset: BOOL = field(init=False, default_factory=BOOL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    ACC: DINT = field(init=False, default_factory=DINT)
    EN: BOOL = field(init=False, default_factory=BOOL)
    TT: BOOL = field(init=False, default_factory=BOOL)
    DN: BOOL = field(init=False, default_factory=BOOL)
    Status: DINT = field(init=False, default_factory=DINT)
    InstructFault: BOOL = field(init=False, default_factory=BOOL)
    PresetInv: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class FBD_TRUNCATE:
    EnableIn: BOOL = field(init=False, default_factory=BOOL)
    Source: REAL = field(init=False, default_factory=REAL)
    EnableOut: BOOL = field(init=False, default_factory=BOOL)
    Dest: DINT = field(init=False, default_factory=DINT)