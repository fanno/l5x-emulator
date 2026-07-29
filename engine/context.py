from dataclasses import dataclass, field

from engine.program import Program
from engine.routine import Routine, RoutineType

from core.timebase import TimeBase

from datatypes.custom.bool import BOOL
from core.emulatorcontext import EmulatorContext

from engine.fbd.sheet import Sheet

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

@dataclass
class ExecutionContext:
    ProgramRef:Program = field(init=True, default=None)
    RoutineRef:Routine = field(init=False, default=None)
    Time:TimeBase = field(init=False, default_factory=TimeBase)
    RungStatus:bool = field(init=True, default=True)
    RungEnabled:bool = field(init=True, default=True)
    Type:RoutineType = field(init=True, default=RoutineType.RLL)
    InputArgs:list = field(init=True, default_factory=list)
    ReturnArgs:list = field(init=True, default_factory=list)
    SFCStatus:BOOL = field(init=True, default_factory=BOOL)
    Context:EmulatorContext = field(init=True, default_factory=EmulatorContext)
    FBD:FBDContext = field(init=True, default_factory=FBDContext)
    RLL:RLLContext = field(init=True, default_factory=RLLContext)
    SFCTransition:bool = field(init=True, default=False)