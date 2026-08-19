from __future__ import annotations

from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from core.registry.datatyperegistry import DataTypeRegistry
from core.l5k.l5kreader import L5KReader

from datatypes.custom.numbers import DINT
from datatypes.custom.bool import BOOL
from datatypes.custom.string import STRING
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

@DataTypeRegistry.register
@dataclass
class MODULEPORT(UDT):
    element: InitVar[Element | None] = None

    Id:DINT = field(init=False, default_factory=DINT)
    Address:STRING = field(init=False, default_factory=STRING)
    Type:STRING = field(init=False, default_factory=STRING)
    Upstream:BOOL = field(init=False, default_factory=BOOL)
    
    def __post_init__(self, element:Element = None):
        if isinstance(element, Element):
            self.Id = DINT(element.get("Id", 0))
            self.Address = STRING(element.get("Address", ""))
            self.Type = STRING(element.get("Type", ""))
            self.Upstream = BOOL(element.get("Upstream", False))

    def toL5X(self, element:Element) -> None:
        pass

    def setValue(self, value:"UDT"):
        pass

@DataTypeRegistry.register
@dataclass
class MODULE(UDT):
    element: InitVar[Element | None] = None

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

    def __post_init__(self, element:Element = None):
        if isinstance(element, Element):
            self.Name = STRING(element.get("Name", ""))
            self.CatalogNumber = STRING(element.get("CatalogNumber", ""))
            self.Vendor = DINT(element.get("Vendor", 0))
            self.ProductType = DINT(element.get("ProductType", 0))
            self.Major = DINT(element.get("Major", 0))
            self.Minor = DINT(element.get("Minor", 0))
            self.ParentModule = STRING(element.get("ParentModule", ""))
            self.ParentModPortId = DINT(element.get("ParentModPortId", 0))
            self.Inhibited = BOOL(element.get("Inhibited", False))
            self.MajorFault = BOOL(element.get("MajorFault", False))

            ports = []
            for port in element.findall("./Ports//Port"):
                ports.append(MODULEPORT(element=port))

            while(len(ports)<2):
                ports.append(MODULEPORT())

            self.Ports = Array[MODULEPORT](MODULEPORT, ports)

    def toL5X(self, element:Element) -> None:
        pass