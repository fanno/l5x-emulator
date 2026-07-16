from xml.etree.ElementTree import Element

from typing import Dict

from core.datatypes import DataTypes
from core.memory.memory import Memory
from core.xml.tags import parseStructure

from opcua.structure import Structure, StructureField, sanitizeName
from opcua.tag import OpcuaTag
from opcua.helpers import *
from opcua.mapping import Mapping

from datatypes.custom.module import MODULE

async def loadModules(root:Element, opcua:OpcuaTag, modules:Dict[str, MODULE], memory:Memory, mapping:Mapping):
    for module in root.findall("./Modules//Module"):
        moduleName = module.get("Name")

        modules[moduleName] = MODULE(module)

        memory.set(moduleName, modules[moduleName])

        if moduleName:
            communications = module.find("./Communications")
            if communications:
                configTag = communications.find("./ConfigTag")
                if configTag:
                    data = configTag.find(f"./Data[@Format='Decorated']")
                    if data:
                        await loadModule(moduleName, "C", data, opcua, memory, mapping)

                connections = communications.findall("./Connections//Connection")
                for connection in connections:
                    if connection:
                        for child in ["InputTag", "OutputTag"]:
                            suffix = connection.get(f"{child}Suffix", None)
                            
                            data = connection.find(f"./{child}/Data[@Format='Decorated']")
                            if data:
                                await loadModule(moduleName, suffix, data, opcua, memory, mapping)

async def loadModule(name:str, suffix:str, element:Element, opcua:OpcuaTag, memory:Memory, mapping:Mapping):
    structure = element.find(f"./Structure")
    if structure:
        dataTypeName = structure.get("DataType", None)
        if suffix is None and ":" in dataTypeName:
            suffix = dataTypeName.split(":")[-2]

        struct = await loadModuleDatatype(dataTypeName, structure, opcua)

        memory.set(f"{name}:{suffix}", parseStructure(structure, struct.name))

async def loadModuleDatatype(name:str, tag:Element, opcua:OpcuaTag) -> Structure:
    struct = Structure(name)
    for member in tag.findall("DataValueMember"):
        dataType = member.get("DataType")
        field = StructureField(name=member.get("Name"),
                                type=getUAVariantType(dataType),
                                dataType=dataType)
        struct.fields.append(field)

    for member in tag.findall("StructureMember"):
        await loadModuleDatatype(member.get("DataType"), member, opcua)
        dataType = sanitizeName(member.get("DataType", None))
        field = StructureField(name=member.get("Name"),
                                type=getUAVariantType(dataType),
                                dataType=dataType)
        struct.fields.append(field)

    ArrayMember = tag.find("ArrayMember")
    if ArrayMember:
        dataType = ArrayMember.get("DataType")

        field = StructureField(name=ArrayMember.get("Name"),
                                type=getUAVariantType(dataType),
                                dataType=dataType,
                                dimension=ArrayMember.get("Dimensions"))
        struct.fields.append(field)

    DataTypes.add(struct)
    await opcua.createDataType(struct)
    return struct
