from typing import Any, Dict, Optional, Type

from dataclasses import dataclass, field

from engine.errors import MajorFault, MinorFault

@dataclass
class LogEvent():
    message: str
    level: str

@dataclass
class UpdateVariableEvent():
    container:str
    path:list[str|int]
    new_value: Any

@dataclass
class StatusScan():
    Max:float = field(init=True, default=0.0)
    Last:float = field(init=True, default=0.0)
    Count:int = field(init=True, default=0)

@dataclass
class StatusEvent():
    EndPoint:float = field(init=True)
    Scan:StatusScan = field(init=True, default_factory=StatusScan)
    Tasks:dict[str, StatusScan] = field(init=True, default_factory=dict)
    Runing:bool = field(init=True, default=False)
    ScanDelayed:float = field(init=True, default=0.0)
    ControllerName:str = field(init=True, default="")
    ControllerType:bool = field(init=True, default="")
    ScanCount:int = field(init=True, default=0)
    Tags:Optional[Dict[str, Type]] = field(init=True, default_factory=dict)

@dataclass
class MinorFaultEvent():
    fault: MinorFault

@dataclass
class MajorFaultEvent():
    fault: MajorFault    