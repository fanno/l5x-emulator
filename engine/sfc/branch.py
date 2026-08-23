from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

@dataclass  
class Branch:
    element: InitVar[Element]

    ID:int = field(init=False, default=None)
    Y:int = field(init=False, default=None)
    BranchType:str = field(init=False, default=None)
    BranchFlow:str = field(init=False, default=None)
    Priority:str = field(init=False, default=None)

    legs:list[int] = field(init=False, default_factory=list)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.ID = int(element.get('ID', '-1'))
            self.Y = int(element.get('Y', '-1'))
            self.BranchType = element.get('BranchType', None)
            self.BranchFlow = element.get('BranchFlow', None)
            self.Priority = element.get('Priority', None)

            for leg in element.findall('.//Leg'):
                self.legs.append(int(leg.get('ID', None)))