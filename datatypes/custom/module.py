from __future__ import annotations

from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL
from datatypes.custom.string import STRING
from datatypes.custom.array import Array

@DataTypeRegistry.register
@dataclass
class MODULEPORT():
    _Element: Element = field(init=True, repr=False, default_factory=lambda: Element(""))

    Id:DINT = field(init=False, default_factory=DINT)
    Address:STRING = field(init=False, default_factory=STRING)
    Type:STRING = field(init=False, default_factory=STRING)
    Upstream:BOOL = field(init=False, default_factory=BOOL)
    
    def __post_init__(self):
        self.Id = DINT(self._Element.get("Id", 0))
        self.Address = STRING(self._Element.get("Address", ""))
        self.Type = STRING(self._Element.get("Type", ""))
        self.Upstream = BOOL(self._Element.get("Upstream", False))

@DataTypeRegistry.register
@dataclass
class MODULE():
    _Element:Element = field(init=True, repr=False, default_factory=lambda: Element(""))

    Name:STRING = field(init=False, default_factory=STRING)
    CatalogNumber:STRING = field(init=False, default_factory=STRING)
    Vendor:DINT = field(init=False, default_factory=DINT)
    ProductType:DINT = field(init=False, default_factory=DINT)
    Major:DINT = field(init=False, default_factory=DINT)
    Minor:DINT = field(init=False, default_factory=DINT)
    ParentModule:STRING = field(init=False, default_factory=STRING)
    ParentModPortId:DINT = field(init=False, default_factory=DINT)
    Inhibited:BOOL = field(init=False, default_factory=BOOL)
    MajorFault:BOOL = field(init=False, default_factory=BOOL)

    Ports:Array[MODULEPORT] = field(init=False, default_factory=lambda: Array.create(MODULEPORT, 2))

    def __post_init__(self):
        self.Name = STRING(self._Element.get("Name", ""))
        self.CatalogNumber = STRING(self._Element.get("CatalogNumber", ""))
        self.Vendor = DINT(self._Element.get("Vendor", 0))
        self.ProductType = DINT(self._Element.get("ProductType", 0))
        self.Major = DINT(self._Element.get("Major", 0))
        self.Minor = DINT(self._Element.get("Minor", 0))
        self.ParentModule = STRING(self._Element.get("ParentModule", ""))
        self.ParentModPortId = DINT(self._Element.get("ParentModPortId", 0))
        self.Inhibited = BOOL(self._Element.get("Inhibited", False))
        self.MajorFault = BOOL(self._Element.get("MajorFault", False))

        ports = []
        for port in self._Element.findall("./Ports//Port"):
            ports.append(MODULEPORT(port))

        while(len(ports)<2):
            ports.append(MODULEPORT())

        self.Ports = Array[MODULEPORT](MODULEPORT, ports)