from xml.etree.ElementTree import Element

from typing import TYPE_CHECKING

from opcua.tag import OpcuaTag
from opcua.mapping import Mapping

if TYPE_CHECKING:    
    from core.memory.memory import Memory
from core.helpers import createMemory
from core.registry.datatyperegistry import DataTypeRegistry
from core.errors import UnhandeledTag, ParseTagException

from datatypes.custom.array import Array
from datatypes.custom.string import STRING
from datatypes.custom.datavariant import DataVariant

def parseStructure(struct_elem: Element, dataType:str = None):
    if dataType is None:
        dataType = struct_elem.get('DataType')

    var = DataTypeRegistry.get(dataType)()
    if isinstance(var, STRING):
        data = struct_elem.find("./DataValueMember[@Name='DATA']")
        if data is None:
            data = struct_elem.find("./Structure/DataValueMember[@Name='DATA']")

        var.setValue(data.text.strip())
    else:
        for child in struct_elem:
            name = child.get('Name')

            if child.tag == 'Structure':
                value = parseStructure(child)
                if name:
                    setattr(var, name, value)
                else:
                    return value
            elif child.tag in ('DataValue', 'DataValueMember'):
                setattr(var, name, parseValue(child))
            elif child.tag == 'StructureMember':
                setattr(var, name, parseStructure(child))
            elif child.tag == 'ArrayMember':
                setattr(var, name, parseArray(child))
            else:
                raise ParseTagException(child.tag, child)
    return var

def parseValue(member_elem: Element):
    data_type = member_elem.get('DataType')
    value_str = member_elem.get('Value')
    return DataTypeRegistry.get(data_type)(value_str)

def getIndex(index:str) -> list[int]:
    i = index.lstrip("[").rstrip("]").split(",")
    return list(map(int, i))

def setArray(data:list, shape:list, value):
    if len(shape) == 1:
        index = shape[0]
        if index >= len(data):
            needed = (index + 1) - len(data)
            data.extend([None] * needed)
            
        data[index] = value
    else:
        current_index = shape[0]
        remaining_shape = shape[1:]
        if current_index >= len(data):
            needed = (current_index + 1) - len(data)
            data.extend([None] * needed)
        if data[current_index] is None or not isinstance(data[current_index], list):
            data[current_index] = []
        setArray(data[current_index], remaining_shape, value)

def parseArray(array: Element):
    dataType = array.get('DataType')
    dt = DataTypeRegistry.get(dataType)

    data = []
    for child in array:
        i = getIndex(child.get("Index"))

        value = parseStructure(child, dataType)

        setArray(data, i, value)
    return Array[dt](dt, data)

async def loadTags(controller:Element, opcua:OpcuaTag, memory:"Memory", mapping:Mapping):
    for tag in controller.findall("./Tags//Tag"):
        await loadTag(tag, opcua, memory, mapping)

async def loadTag(tag:Element, opcua:OpcuaTag, memory:"Memory", mapping:Mapping):
    name = tag.get('Name')

    decorated = tag.find("Data[@Format='Decorated']")
    if decorated is not None:
        passStructures = ['Structure', 'DataValue']

        for s in passStructures:
            element = decorated.find(s)
            if element is not None:
                val = parseStructure(element)
                memory.set(name, val)
                break
        if element is None:
            array = decorated.find('Array')
            if array is not None:
                memory.set(name, parseArray(array))
            else:
                raise UnhandeledTag(name, decorated, element)
    else:
        datatype = tag.get('DataType')

        value = DataTypeRegistry.get(datatype)()

        data = tag.find('./Data')
        if data:
            params = data.find('.*')
            if params:
                for k,v in params.attrib.items():
                    if hasattr(value, k):
                        attr = getattr(value, k)
                        if isinstance(attr , DataVariant):
                            attr.setValue(v)
                        else:
                            raise UnhandeledTag(k, v, params)
                    else:
                        raise UnhandeledTag(k, v, params)
        memory.set(name, value)

async def createTagsMemory(opcua:OpcuaTag, memory:"Memory", mapping:Mapping):
    for name, tag in opcua.tags.items():
        await createMemory(tag, opcua, memory, mapping)
