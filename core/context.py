from dataclasses import dataclass, field

from engine.program import Program

from core.timebase import TimeBase

@dataclass
class ExecutionContext:
    Time:TimeBase = field(default_factory=TimeBase)
    RungStatus:bool = field(init=False, default=True)
    RungEnabled:bool = field(init=False, default=True)
    ProgramRef:Program = field(init=False, default=None)
    Jump:str = field(init=False, default=None)