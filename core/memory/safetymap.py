

from dataclasses import dataclass, field

from lxml.etree import _Element as Element

@dataclass
class SafetyMap():
    _Element: Element = field(init=True, repr=False, default=None)

    Pairs:dict[str, str] = field(init=False, default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self._Element, Element):
            if self._Element.text:
                pairs = self._Element.text.split(',')
                for pair in pairs:
                    pair = pair.strip().split('=')
                    self.Pairs[pair[0]] = pair[1]