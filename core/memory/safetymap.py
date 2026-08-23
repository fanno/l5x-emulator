from dataclasses import dataclass, field, InitVar

from lxml.etree import _Element as Element

@dataclass
class SafetyMap():
    element: InitVar[Element]=None

    Pairs:dict[str, str] = field(init=False, default_factory=dict)
    
    def __post_init__(self, element:Element=None):
        if isinstance(element, Element):
            if element.text:
                pairs = element.text.split(',')
                for pair in pairs:
                    pair = pair.strip().split('=')
                    self.Pairs[pair[0]] = pair[1]