from __future__ import annotations

from typing import Union
from dataclasses import dataclass, field

from datatypes.custom.types import DataType as DT

@dataclass
class UIMemory:
    Name:str = field(init=True)
    Datatype:DT = field(init=True, default=DT.UNKNOWN)
    Value:MemoryValues = None

@dataclass
class UIMemoryPrimitive(UIMemory):
    Value:Primitive = field(init=True, default=None)

    def update(self, new:UIMemoryPrimitive) -> None:
        if isinstance(new, UIMemoryPrimitive):
            self.Value = new.Value

@dataclass
class UIMemoryObject(UIMemory):
    Class:str = field(init=True, default=None)
    Value:dict[str, MemoryType] = field(init=True, default_factory=dict)

    def update(self, new:UIMemoryObject) -> None:
        if isinstance(new, UIMemoryObject):
            for name, item in new.Value.items():
                if name in self.Value:
                    self.Value[name].update(item)

Primitive = Union[int, float, bool, str]
MemoryType = Union[UIMemoryPrimitive, UIMemoryObject]

MemoryValues = Union[dict[str, MemoryType], Primitive, None]