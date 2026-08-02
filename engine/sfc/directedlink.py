from typing import Any

from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

@dataclass  
class DirectedLink:
    _Element: Element = field(init=True)

    FromID:int = field(init=False, default=-1)
    ToID:int = field(init=False, default=-1)

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.FromID = int(self._Element.get('FromID', '-1'))
            self.ToID = int(self._Element.get('ToID', '-1'))