from dataclasses import dataclass, field

from engine.program import Program
from engine.routine import Routine, RoutineType

from core.timebase import TimeBase

from datatypes.custom.bool import BOOL

from engine.fbd.sheet import Sheet
from datatypes.sfc import SFC_STEP
from datatypes.custom.numbers import INT

'''
    SFCStatus:BOOL = field(init=True, default_factory=BOOL)
    SFCTransition:bool = field(init=True, default=False)

'''
class EmulatorContext():
    preScan:bool
    postScan:bool

    def __init__(self, pre:bool=False, post:bool=False):
        self.preScan = pre
        self.postScan = post

@dataclass
class SFCContext:
    Paused: INT = field(init=False, default_factory=INT)
    Resuming: INT = field(init=False, default_factory=INT)
    Step: SFC_STEP = field(init=False, default_factory=SFC_STEP)
    Status:BOOL = field(init=True, default_factory=BOOL)
    Transition:bool = field(init=True, default=False)

@dataclass
class FBDContext:
    sheet:Sheet = field(init=True, default_factory=Sheet)

@dataclass
class RLLContext:
    EOT:bool = field(init=True, default=False)
    TND:bool = field(init=True, default=False)
    PSC:bool = field(init=True, default='')
    PSR:str = field(init=True, default='False')
    Jump:str = field(init=False, default=None)
    inMCR:bool = field(init=False, default=False)
    MCRActive:bool = field(init=False, default=False)
    RungEnabled:bool = field(init=True, default=True)
    RungStatus:bool = field(init=True, default=True)    

@dataclass
class ExecutionContext:
    ProgramRef:Program = field(init=True, default=None)
    RoutineRef:Routine = field(init=False, default=None)
    Time:TimeBase = field(init=False, default_factory=TimeBase)
    Type:RoutineType = field(init=True, default=RoutineType.RLL)
    InputArgs:list = field(init=True, default_factory=list)
    ReturnArgs:list = field(init=True, default_factory=list)
    
    Context:EmulatorContext = field(init=True, default_factory=EmulatorContext)
    FBD:FBDContext = field(init=True, default_factory=FBDContext)
    RLL:RLLContext = field(init=True, default_factory=RLLContext)
    SFC:SFCContext = field(init=True, default_factory=SFCContext)