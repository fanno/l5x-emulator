from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

@dataclass  
class DirectedLink:
    element: InitVar[Element]

    FromID:int = field(init=False, default=-1)
    ToID:int = field(init=False, default=-1)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.FromID = int(element.get('FromID', '-1'))
            self.ToID = int(element.get('ToID', '-1'))