from lxml.etree import _Element as Element

from typing import Dict

from core.datatypes import DataTypes
from core.memory.memory import Memory, TagMetadata, OpcUaAccess
from core.xml.tags import parseStructure

from opcua.structure import Structure, StructureField, sanitizeName
from opcua.tag import OpcuaTag
from opcua.helpers import *
from opcua.mapping import Mapping

from datatypes.custom.module import MODULE

from core.events import LoadingEvent
from eventbus.eventbus import EventBus

async def loadModules(root:Element, opcua:OpcuaTag, modules:Dict[str, MODULE], memory:Memory, mapping:Mapping):
    for module in root.findall("./Modules//Module"):
        moduleName = module.get("Name")
        SafetyEnabled = BOOL.toValue(module.get("SafetyEnabled"))

        EventBus.get().dispatch(LoadingEvent(f"Module: {moduleName}"))

        mod = MODULE(element=module)
        address:str = None

        for port in mod.Ports:
            if port.Type == "PointIO":
                address = port.Address.getPLCValue()
                break

        parent = mod.ParentModule.getPLCValue()

        modules[moduleName] = mod

        memory.set(moduleName, modules[moduleName])
        if moduleName:
            if parent != "Local":
                moduleName = parent

            communications = module.find("./Communications")
            if isinstance(communications, Element):
                configTag = communications.find("./ConfigTag")
                if isinstance(configTag, Element):
                    medatata = TagMetadata(OpcUa_Access=OpcUaAccess.from_string(configTag.get("OpcUaAccess")))

                    data = configTag.find(f"./Data[@Format='Decorated']")
                    if isinstance(data, Element):
                        path = modulePath(moduleName, address, "C")

                        await loadModule(path, data, opcua, memory, mapping, medatata)

                connections = communications.find("./Connections")
                if isinstance(connections, Element):
                    rackConnection = connections.find("./RackConnection")
                    if isinstance(rackConnection, Element):
                        inAliasTag = rackConnection.find("./InAliasTag")
                        if isinstance(inAliasTag, Element):
                            if address:
                                path = modulePath(moduleName, address, "I")
                                memPath = f'{modulePath(moduleName, None, "I")}.Data'
                                data = memory.get(memPath)
                                memory.set(path, data[int(address)])

                        outAliasTag = rackConnection.find("./OutAliasTag")
                        if isinstance(outAliasTag, Element):
                            if address:
                                path = modulePath(moduleName, address, "O")
                                memPath = f'{modulePath(moduleName, None, "O")}.Data'
                                data = memory.get(memPath)
                                memory.set(path, data[int(address)])

                    allConnection = connections.findall(".//Connection")
                    for connection in allConnection:
                        if isinstance(connection, Element):
                            for child in ["InputTag", "OutputTag"]:
                                suffix = connection.get(f"{child}Suffix", None)
                                if suffix is None:
                                    if SafetyEnabled:
                                        suffix = "S"
                                    elif child == "InputTag":
                                        suffix = "I"
                                    else:
                                        suffix = "O"

                                tag = connection.find(f"./{child}")
                                if isinstance(tag, Element):
                                    medatata = TagMetadata(OpcUa_Access=OpcUaAccess.from_string(tag.get("OpcUaAccess")))

                                    data = tag.find(f"./Data[@Format='Decorated']")
                                    if isinstance(data, Element):
                                        path = modulePath(moduleName, address, suffix)
                                        await loadModule(path, data, opcua, memory, mapping, medatata)

def modulePath(name:str, address:str=None, suffix:str=None) -> str:
    if address is None or address == "0":
        address = ""

    if address != "":
        address = f":{address}"

    if suffix:
        suffix = f":{suffix}"

    return f"{name}{address}{suffix}"

async def loadModule(path:str, element:Element, opcua:OpcuaTag, memory:Memory, mapping:Mapping, medatata:TagMetadata = TagMetadata()):
    structure = element.find(f"./Structure")
    if isinstance(structure, Element):
        dataTypeName = structure.get("DataType", None)

        struct = await loadModuleDatatype(dataTypeName, structure, opcua)

        value = parseStructure(structure, struct.name)

        memory.set(path, value)
        memory.set_metadata(path, medatata)

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
    if isinstance(ArrayMember, Element):
        dataType = ArrayMember.get("DataType")

        field = StructureField(name=ArrayMember.get("Name"),
                                type=getUAVariantType(dataType),
                                dataType=dataType,
                                dimension=ArrayMember.get("Dimensions"))
        struct.fields.append(field)

    DataTypes.add(struct)
    await opcua.createDataType(struct)
    return struct
