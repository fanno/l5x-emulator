from typing import Any

from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

@dataclass  
class Wire:
    element: InitVar[Element]

    FromID:int = field(init=False, default=None)
    ToID:int = field(init=False, default=None)
    ToParam:str = field(init=False, default=None)
    FromParam:str = field(init=False, default=None)
    ID:int = field(init=False, default=None)

    Value:Any = field(init=False, default=None)

    _idx: int = 1

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.ID = Wire._idx
            Wire._idx += 1

            self.FromID = int(element.get('FromID', '-1'))
            self.ToID = int(element.get('ToID', '-1'))
            self.ToParam = element.get('ToParam', None)
            self.FromParam = element.get('FromParam', None)