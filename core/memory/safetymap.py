

from dataclasses import dataclass, field

from xml.etree.ElementTree import Element

@dataclass
class SafetyMap():
    _Element: Element = field(init=True, repr=False, default_factory=lambda: Element(""))

    Pairs:dict[str, str] = field(init=False, default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self._Element, Element):
            if self._Element.text:
                pairs = self._Element.text.split(',')
                for pair in pairs:
                    pair = pair.strip().split('=')
                    self.Pairs[pair[0]] = pair[1]