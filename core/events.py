from typing import Any, Dict, Optional, Type, Union

from dataclasses import dataclass, field

from engine.errors import MajorFault, MinorFault

@dataclass
class LogEvent():
    message: str
    level: str

@dataclass
class UpdateVariableEvent():
    Container:str
    path:list[str|int]
    new_value: Any

@dataclass
class StatusScan():
    Max:float = field(init=True, default=0.0)
    Last:float = field(init=True, default=0.0)
    Count:int = field(init=True, default=0)

@dataclass
class StatusRequestEvent():
    Initial:bool = field(init=True, default=False)
    Paths: Union[list[str], dict[str, dict]] = field(init=True, default_factory=dict)
    Container:str = field(init=True, default=None)

    def __post_init__(self):
        if isinstance(self.Paths, list):
            self.Paths = paths_to_nested_filter(self.Paths)

def paths_to_nested_filter(paths: list[str] | None) -> dict[str, dict]:
    if paths is None:
        return {}
    
    result: dict[str, dict] = {}
    
    for path_str in paths:
        parts = path_str.split('.')
        
        current = result
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        leaf_key = parts[-1]
        if leaf_key not in current:
            current[leaf_key] = {}
    
    return result

@dataclass
class StatusEvent():
    EndPoint:str = field(init=True, default=None)
    Scan:StatusScan = field(init=True, default_factory=StatusScan)
    OpcUaRead:StatusScan = field(init=True, default_factory=StatusScan)
    OpcUaWrite:StatusScan = field(init=True, default_factory=StatusScan)
    Tasks:dict[str, StatusScan] = field(init=True, default_factory=dict)
    Programs:dict[str, dict[str, StatusScan]] = field(init=True, default_factory=dict)
    Runing:bool = field(init=True, default=False)
    ScanDelayed:float = field(init=True, default=0.0)
    ControllerName:str = field(init=True, default="")
    ControllerType:bool = field(init=True, default="")
    ScanCount:int = field(init=True, default=0)
    Tags:Optional[Dict[str, Type]] = field(init=True, default_factory=dict)
    StatusRequest:StatusRequestEvent = field(init=True, default_factory=StatusRequestEvent)

@dataclass
class LoadingEvent():
    Loading:str = field(init=True)

@dataclass
class MinorFaultEvent():
    fault: MinorFault

@dataclass
class MajorFaultEvent():
    fault: MajorFault