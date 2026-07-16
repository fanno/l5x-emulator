from xml.etree.ElementTree import Element

from asyncua import ua

from core.datatypes import DataTypes
from core.registry.datatyperegistry import DataTypeRegistry

from opcua.structure import Structure, StructureField
from opcua.tag import OpcuaTag
from opcua.helpers import *

async def loadDataTypes(controller:Element, opcua:OpcuaTag):
    process = True
    while process:
        process = False
        for tag in controller.findall("./DataTypes//DataType"):
            name = tag.get("Name")
            if not DataTypes.has(name):
                if _canCreateDataType(tag):
                    struct = Structure(name=name)
                    if tag.get("Family") == "StringFamily":
                        struct.type = ua.VariantType.String
                        struct.base = (DataTypeRegistry.get("STRING"),)

                    members = tag.findall("./Members//Member")
                    for member in members:
                        if member.get("Hidden") == "false":
                            dataType = member.get("DataType")

                            field = StructureField(name=member.get("Name"),
                                                   type=getUAVariantType(dataType),
                                                   dataType=dataType,
                                                   dimension=member.get("Dimension", []))
                            struct.fields.append(field)

                    DataTypes.add(struct)
                    await opcua.createDataType(struct)
                process = True

def _canCreateDataType(tag:Element):
    name = tag.get("Name")
    if DataTypes.has(name):
        return False
    
    if tag.get("Family") == "StringFamily":
        return True

    members = tag.findall("./Members//Member")
    for member in members:
        if member.get("Hidden") == "false":
            dt = member.get("DataType")
            if not DataTypes.has(dt):
                return False
    return True