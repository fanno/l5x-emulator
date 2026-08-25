from lxml.etree import _Element as Element

from opcua.structure import Structure, StructureField, sanitizeName
from opcua.helpers import getUAVariantType
from core.datatypes import DataTypes
from core.registry.instructionregistry import InstructionRegistry
from opcua.tag import OpcuaTag

from engine.aoi.aoi import AOI, AOIRegistry

from engine.aoi.aoi import AOI_CLASS    

from datatypes.custom.udt import AOI_UDT

from core.events import LoadingEvent
from eventbus.eventbus import EventBus

async def loadAoiDefinition(controller:Element, opcua:OpcuaTag) -> int:
    loaded:int = 0
    process = True
    while process:
        process = False
        for instruction in controller.findall("./AddOnInstructionDefinitions//AddOnInstructionDefinition"):
            name = instruction.get("Name")
            if not InstructionRegistry.has(name):
                if _canCreateAOI(instruction):
                    AOIRegistry.register(AOI(element=instruction))
                    
                    EventBus.get().dispatch(LoadingEvent(f"AOI: {name}"))

                    parameters = instruction.findall("./Parameters//Parameter")
                    localTags = instruction.findall("./LocalTags//LocalTag")
                    
                    struct = Structure(name)

                    EnableIn = next((p for p in parameters if p.get("Name") == "EnableIn"), None)
                    if isinstance(EnableIn, Element):
                        struct.fields.append(createField(EnableIn))
                        parameters.remove(EnableIn)

                    EnableOut = next((p for p in parameters if p.get("Name") == "EnableOut"), None)
                    if isinstance(EnableOut, Element):
                        struct.fields.append(createField(EnableOut))
                        parameters.remove(EnableOut)

                    for parameter in [p for p in parameters if p.get("Usage") == "Input" and p.get("DataType") == "BOOL"]:
                        if isinstance(parameter, Element):
                            struct.fields.append(createField(parameter))
                            parameters.remove(parameter)

                    for parameter in [p for p in parameters if p.get("Usage") == "Output" and p.get("DataType") == "BOOL"]:
                        if isinstance(parameter, Element):
                            struct.fields.append(createField(parameter))
                            parameters.remove(parameter)

                    for localTag in [p for p in localTags if p.get("DataType") == "BOOL"]:
                        if isinstance(localTag, Element):
                            struct.fields.append(createField(localTag))
                            localTags.remove(localTag)

                    for parameter in [p for p in parameters if p.get("Usage") == "Input" or p.get("Usage") == "Output"]:
                        if isinstance(parameter, Element):
                            struct.fields.append(createField(parameter))
                            parameters.remove(parameter)

                    for localTag in localTags[:]:
                        if isinstance(localTag, Element):
                            struct.fields.append(createField(localTag))
                            localTags.remove(localTag)

                    struct.base = (AOI_UDT,)
                    DataTypes.add(struct)
                    InstructionRegistry.register_local(AOI_CLASS, name)
                    process = True
                    loaded += 1

    await opcua.createDataTypes()
    return loaded

def createField(element:Element)  -> StructureField:
    dataType = element.get("DataType")
    usage = element.get("Usage", "Local")
    return StructureField(name=element.get("Name"), type=getUAVariantType(dataType), dataType=dataType, usage=usage)

def _canCreateAOI(tag:Element):
    parameters = tag.findall("./Parameters//Parameter")
    for parameter in parameters:
        if not DataTypes.has(parameter.get("DataType")):
            return False
        
    localTags = tag.findall("./LocalTags//LocalTag")    
    for localTag in localTags:
        if not DataTypes.has(localTag.get("DataType")):
            return False
    return True