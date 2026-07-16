from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import INT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class AB_PowerFlex525V_EENET_Drive_I_0:
    DriveStatus: INT = field(init=False, default_factory=INT)
    Ready: BOOL = field(init=False, default_factory=BOOL)
    Active: BOOL = field(init=False, default_factory=BOOL)
    CommandDir: BOOL = field(init=False, default_factory=BOOL)
    ActualDir: BOOL = field(init=False, default_factory=BOOL)
    Accelerating: BOOL = field(init=False, default_factory=BOOL)
    Decelerating: BOOL = field(init=False, default_factory=BOOL)
    Faulted: BOOL = field(init=False, default_factory=BOOL)
    AtReference: BOOL = field(init=False, default_factory=BOOL)
    CommFreqCnt: BOOL = field(init=False, default_factory=BOOL)
    CommLogicCnt: BOOL = field(init=False, default_factory=BOOL)
    ParmsLocked: BOOL = field(init=False, default_factory=BOOL)
    DigIn1Active: BOOL = field(init=False, default_factory=BOOL)
    DigIn2Active: BOOL = field(init=False, default_factory=BOOL)
    DigIn3Active: BOOL = field(init=False, default_factory=BOOL)
    DigIn4Active: BOOL = field(init=False, default_factory=BOOL)
    OutputFreq: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class AB_PowerFlex525V_EENET_Drive_O_0:
    LogicCommand: INT = field(init=False, default_factory=INT)
    Stop: BOOL = field(init=False, default_factory=BOOL)
    Start: BOOL = field(init=False, default_factory=BOOL)
    Jog: BOOL = field(init=False, default_factory=BOOL)
    ClearFaults: BOOL = field(init=False, default_factory=BOOL)
    Forward: BOOL = field(init=False, default_factory=BOOL)
    Reverse: BOOL = field(init=False, default_factory=BOOL)
    ForceKeypadCtrl: BOOL = field(init=False, default_factory=BOOL)
    MOPIncrement: BOOL = field(init=False, default_factory=BOOL)
    AccelRate1: BOOL = field(init=False, default_factory=BOOL)
    AccelRate2: BOOL = field(init=False, default_factory=BOOL)
    DecelRate1: BOOL = field(init=False, default_factory=BOOL)
    DecelRate2: BOOL = field(init=False, default_factory=BOOL)
    FreqSel01: BOOL = field(init=False, default_factory=BOOL)
    FreqSel02: BOOL = field(init=False, default_factory=BOOL)
    FreqSel03: BOOL = field(init=False, default_factory=BOOL)
    MOPDecrement: BOOL = field(init=False, default_factory=BOOL)
    FreqCommand: INT = field(init=False, default_factory=INT)
