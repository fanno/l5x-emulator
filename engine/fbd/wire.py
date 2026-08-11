from typing import Any

from lxml.etree import _Element as Element

from dataclasses import dataclass, field

@dataclass  
class Wire:
    _Element: Element = field(init=True)

    FromID:int = field(init=False, default=None)
    ToID:int = field(init=False, default=None)
    ToParam:str = field(init=False, default=None)
    FromParam:str = field(init=False, default=None)
    ID:int = field(init=False, default=None)

    Value:Any = field(init=False, default=None)

    _idx: int = 1

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.ID = Wire._idx
            Wire._idx += 1

            self.FromID = int(self._Element.get('FromID', '-1'))
            self.ToID = int(self._Element.get('ToID', '-1'))
            self.ToParam = self._Element.get('ToParam', None)
            self.FromParam = self._Element.get('FromParam', None)