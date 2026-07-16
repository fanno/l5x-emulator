from dataclasses import dataclass, field

from engine.program import Program
from engine.routine import Routine, RoutineType

from core.timebase import TimeBase

from datatypes.custom.bool import BOOL

@dataclass
class ExecutionContext:
    ProgramRef:Program = field(init=True, default=None)
    RoutineRef:Routine = field(init=False, default=None)
    Time:TimeBase = field(init=False, default_factory=TimeBase)
    RungStatus:bool = field(init=True, default=True)
    RungEnabled:bool = field(init=True, default=True)
    Jump:str = field(init=False, default=None)
    Type:RoutineType = field(init=True, default=RoutineType.RLL)
    InputArgs:list = field(init=True, default_factory=list)
    ReturnArgs:list = field(init=True, default_factory=list)
    SFCStatus:BOOL = field(init=True, default_factory=BOOL)
    EOT:bool = field(init=True, default=False)
    TND:bool = field(init=True, default=False)
    SFCTransition:bool = field(init=True, default=False)
    inMCR:bool = field(init=False, default=False)
    MCRActive:bool = field(init=False, default=False)