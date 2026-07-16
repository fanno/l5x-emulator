from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT, SINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class AB_1734_SSI_C_1:
    Run: SINT = field(init=False, default_factory=SINT)
    GrayBinary: SINT = field(init=False, default_factory=SINT)
    WordLength: SINT = field(init=False, default_factory=SINT)
    DataSpeed: SINT = field(init=False, default_factory=SINT)
    G2BConvert: SINT = field(init=False, default_factory=SINT)
    Standard: SINT = field(init=False, default_factory=SINT)
    SSIWordDelayTime: INT = field(init=False, default_factory=INT)
    Trailing: SINT = field(init=False, default_factory=SINT)
    InputLatchCtrl: SINT = field(init=False, default_factory=SINT)
    InputLatch_0: BOOL = field(init=False, default_factory=BOOL)
    InputLatch_1: BOOL = field(init=False, default_factory=BOOL)
    SensorResolution: INT = field(init=False, default_factory=INT)
    SensorCycle: INT = field(init=False, default_factory=INT)
    SSIWordFilterCtrl: SINT = field(init=False, default_factory=SINT)
    Compare0Value: DINT = field(init=False, default_factory=DINT)
    Compare1Value: DINT = field(init=False, default_factory=DINT)
    Compare0Control: SINT = field(init=False, default_factory=SINT)
    Compare0_0: BOOL = field(init=False, default_factory=BOOL)
    Compare0_1: BOOL = field(init=False, default_factory=BOOL)
    Compare1Control: SINT = field(init=False, default_factory=SINT)
    Compare1_0: BOOL = field(init=False, default_factory=BOOL)
    Compare1_1: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_1734_SSI_I_0:
    Fault: DINT = field(init=False, default_factory=DINT)
    PresentData: DINT = field(init=False, default_factory=DINT)
    LatchedData: DINT = field(init=False, default_factory=DINT)
    Status: INT = field(init=False, default_factory=INT)
    InputStatus: BOOL = field(init=False, default_factory=BOOL)
    Run: BOOL = field(init=False, default_factory=BOOL)
    DecreasingCount: BOOL = field(init=False, default_factory=BOOL)
    IncreasingCount: BOOL = field(init=False, default_factory=BOOL)
    Compare0Reached: BOOL = field(init=False, default_factory=BOOL)
    Compare1Reached: BOOL = field(init=False, default_factory=BOOL)
    Compare0Status: BOOL = field(init=False, default_factory=BOOL)
    Compare1Status: BOOL = field(init=False, default_factory=BOOL)
    PowerFault: BOOL = field(init=False, default_factory=BOOL)
    ConfigFault: BOOL = field(init=False, default_factory=BOOL)
    CommFault: BOOL = field(init=False, default_factory=BOOL)
    InputDataFault: BOOL = field(init=False, default_factory=BOOL)
    DataLatched: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class AB_1734_SSI_O_0:
    Control: SINT = field(init=False, default_factory=SINT)
    LatchAck: BOOL = field(init=False, default_factory=BOOL)
    Compare0Ack: BOOL = field(init=False, default_factory=BOOL)
    Compare1Ack: BOOL = field(init=False, default_factory=BOOL)
    Compare0Select: BOOL = field(init=False, default_factory=BOOL)
    Compare1Select: BOOL = field(init=False, default_factory=BOOL)
