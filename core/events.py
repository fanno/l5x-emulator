from typing import Any, Dict, Optional, Type

from dataclasses import dataclass, field

@dataclass
class LogEvent():
    message: str

@dataclass
class UpdateVariableEvent():
    container:str
    path:list[str|int]
    new_value: Any

@dataclass
class StatusEvent():
    EndPoint:float = field(init=True)

    Runing:bool = field(init=True, default=False)
    ScanMax:float = field(init=True, default=0.0)
    ScanCurrent:float = field(init=True, default=0.0)
    ScanDelayed:float = field(init=True, default=0.0)
    ControllerName:str = field(init=True, default="")
    ControllerType:bool = field(init=True, default="")
    ScanCount:int = field(init=True, default=0)
    Data:Optional[Dict[str, Type]] = field(init=True, default_factory=dict)