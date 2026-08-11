from lxml.etree import _Element as Element

from dataclasses import dataclass, field

@dataclass  
class Branch:
    _Element: Element = field(init=True)

    ID:int = field(init=False, default=None)
    Y:int = field(init=False, default=None)
    BranchType:str = field(init=False, default=None)
    BranchFlow:str = field(init=False, default=None)
    Priority:str = field(init=False, default=None)

    legs:list[int] = field(init=False, default_factory=list)

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.ID = int(self._Element.get('ID', '-1'))
            self.Y = int(self._Element.get('Y', '-1'))
            self.BranchType = self._Element.get('BranchType', None)
            self.BranchFlow = self._Element.get('BranchFlow', None)
            self.Priority = self._Element.get('Priority', None)

            for leg in self._Element.findall('.//Leg'):
                self.legs.append(int(leg.get('ID', None)))