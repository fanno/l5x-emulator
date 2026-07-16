from asyncua import ua, Node

from typing import TYPE_CHECKING

from opcua.mapping import Mapping
from opcua.tag import OpcuaTag, Tag
from opcua.helpers import *

from datatypes.custom.datavariant import DataVariant

from core.registry.datatyperegistry import DataTypeRegistry
from core.signal import Signal

if TYPE_CHECKING:
    from core.memory.memory import Memory

async def createMemory(tag: Tag, opcua:OpcuaTag, memory:"Memory", mapping:Mapping, parentPath:list = None, parent:Node = None) ->  None:
    if parentPath is None:
        parentPath = []

    result = None
    
    current_path = parentPath + [tag.Name]
    variant_type = getUAVariantType(tag.DataType)

    if tag.PLC:
        result = tag.PLC
    elif DataTypeRegistry.has(tag.DataType):
        result = DataTypeRegistry.get(tag.DataType)()
    elif variant_type in (ua.VariantType.ExtensionObject, ua.VariantType.String, ua.VariantType.DateTime):
        result = DataTypeRegistry.get(tag.DataType)()
    else:
        result = tag.Variant.Value

    memory.set(current_path, result)

    node = await opcua.createTag(tag, parent)

    signal = Signal(PATH=current_path,
                    NODE=node)
    mapping.add(signal)

    for t in tag.Children:
        att = await createMemory(tag=t,
                                 opcua=opcua,
                                 memory=memory,
                                 mapping=mapping,
                                 parentPath=current_path,
                                 parent=node)

        setattr(result, t.Name, att)

    memory.set(current_path, result)

    if isinstance(result, DataVariant):
        #result.fromVariant(tag.Variant)
        await node.write_value(result.toVariant())
    else:
        await node.write_value(ua.Variant(result, variant_type))

    return result

