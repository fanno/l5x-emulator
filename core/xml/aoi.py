from xml.etree.ElementTree import Element

from opcua.structure import Structure, StructureField
from opcua.helpers import getUAVariantType
from core.datatypes import DataTypes

from core.registry.instructionregistry import InstructionRegistry
from opcua.tag import OpcuaTag

from engine.aoi.aoi import AOI, AOIRegistry

from engine.aoi.aoi import AOI_CLASS    

async def loadAoiDefinition(controller:Element, opcua:OpcuaTag):

    for instruction in controller.findall("./AddOnInstructionDefinitions//AddOnInstructionDefinition"):
        AOIRegistry.register(AOI(_Element=instruction))

        name = instruction.get("Name")
        parameters = instruction.findall("./Parameters//Parameter")
        
        struct = Structure(name)
        for parameter in parameters:
            usage = parameter.get("Usage")
            if usage == "Input" or usage == "Output":
                dataType = parameter.get("DataType")
                
                field = StructureField(parameter.get("Name"), getUAVariantType(dataType), dataType)
                struct.fields.append(field)

        DataTypes.add(struct)

        InstructionRegistry.register(AOI_CLASS, name)
    await opcua.createDataTypes()