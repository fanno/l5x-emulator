from __future__ import annotations
import logging

from typing import Dict, Any, Set

from dataclasses import dataclass, field, fields

from lxml.etree import _Element as Element

from asyncua import Server, Node, ua
from asyncua.common.structures104 import new_struct, new_struct_field


from opcua.structure import Structure, StructureField, sanitizeName
from opcua.helpers import *
from opcua.mapping import Mapping

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array

from core.signal import Signal
from core.memory.memory import Memory, OpcUaAccess
from core.datatypes import DataTypes, DataTypeRegistry

from opcua.updater import OPCUAUpdater

from protocols.memory import SupportsSetValue
from protocols.opcua import SupportsVariant, SupportsOPCUA

from utils.isplcinstance import isPLCInstance

async def create_struct(struct:Structure, server:Server, id):
    newFields:list[StructureField] = []
    
    for field in struct.fields:
        if field.usage != "Local":
            struct_field = new_struct_field(name=field.name,
                                            dtype=field.type,
                                            array=bool(field.dimension))

            newFields.append(struct_field)

    struct.snode, struct.nodeid = await new_struct(
        server,
        id,
        struct.name,
        newFields
    )

@dataclass
class OpcuaTag:
    SERVER:Server = field(init=True)
    NAME:str = field(init=True)
    memory:Memory = field(init=True)
    mapping:Mapping = field(init=True)
    updater:Set[OPCUAUpdater] = field(init=False, default_factory=set)

    __folder:Node =  field(init=False, default=None)
    __idx: int =  field(init=False, default=None)
    tags: Dict[str, Tag] = field(init=False, default_factory=lambda : {})

    async def registerNamespace(self, namespace:str) -> None:
        self.__idx = await self.SERVER.register_namespace(namespace)

    async def createFolder(self, folder:Node) -> None:
        self.__folder = await self.SERVER.nodes.objects.add_folder(self.getIDX(), folder)

    def getFolder(self) -> Node:
        if self.__folder is None:
            raise RuntimeError(f"call createFolder first")
        return self.__folder

    def getIDX(self) -> int:
        if self.__idx is None:
            raise RuntimeError(f"call registerNamespace first")
        return self.__idx

    async def createTag(self, tag: Tag, parent:Node = None) -> Node:
        logging.debug(f"OpcuaTag.createTag: {tag}")
        if parent is None:
            parent = self.getFolder()

        if getUAVariantType(tag.DataType) == ua.VariantType.ExtensionObject:
            ot = await parent.add_variable(self.getIDX(), tag.Name, ua.Variant(getattr(ua, tag.DataType)(), ua.VariantType.ExtensionObject))
        else:
            ot = await parent.add_variable(self.getIDX(), tag.Name, tag.Variant)
        await ot.set_writable()
        return ot

    async def createNodes(self, forceOpcua:bool = False):
        for k, v in self.memory.getMemoryAll().items():
            medatata = self.memory.get_metadata(k)
            if medatata:
                if medatata.OpcUa_Access != OpcUaAccess.NONE or forceOpcua:
                    await self.createNode(k, v)

    async def createNode(self, name:str, value: Any, path:list = [], parent:Node = None):
        if parent is not None:
            # TODO should we only have root node ?
            return
        if parent is None:
            parent = self.getFolder()
        
        node = await self._createVariantNode(parent, name, value)
        
        if node is None:
            return None
        
        await node.set_writable()
        if node:
            current_path = path + [name]
            logging.debug(f"created Node: {current_path} ({type(value).__name__})")

            signal = Signal(PATH=current_path,
                            NODE=node,
                            MEMORY=value)
            self.mapping.add(signal)

            if not isinstance(value, DataVariant):
                for field in fields(value):
                    if field.repr:
                        field_name = field.name
                        await self.createNode(
                            name=field_name,
                            value=getattr(value, field_name),
                            path=current_path,
                            parent=node
                        )

            if isPLCInstance(value, SupportsOPCUA):
                value.setOPCUAOUdater(self.updater, signal, self.memory)
        
    async def _createVariantNode(self, parent: Node, name: str, value: Any) -> Optional[Node]:
        if isPLCInstance(value, SupportsVariant):
            dataNode = None
            if value._ua_variant == ua.VariantType.ExtensionObject:
                dt_name = value.__class__.__name__
                if hasattr(ua, dt_name) or hasattr(ua, dt_name.upper()):
                    dt = DataTypes.get(dt_name)
                    dataNode = dt.snode.nodeid
            return await parent.add_variable(self.getIDX(), name, value.toVariant(), datatype=dataNode)

        raise RuntimeError(f"Unsupported value type '{type(value).__name__}' for tag '{name}' Expected SupportsVariant")

    async def createDataType(self, struct:Structure) -> None:
        await create_struct(struct, self.SERVER, self.getIDX())

        custom_objs = await self.SERVER.load_data_type_definitions()

    async def createDataTypes(self) -> None:
        process = True
        while process:
            process = False
            for struct_name, struct in DataTypes.getAll().items():
                if struct.datavariant:
                    continue

                if struct.nodeid == 0:
                    create = True
                    for field in struct.fields:
                        if field.type == ua.VariantType.ExtensionObject:
                            if field.dataType in DataTypes.getAll():
                                if DataTypes.get(field.dataType).snode == 0:
                                    create = False
                                    break

                    if create:
                        await create_struct(struct, self.SERVER, self.getIDX())
                    else:
                        process = True

        custom_objs = await self.SERVER.load_data_type_definitions()

@dataclass
class Tag:
    Name: str = field(init=True)
    DataType: str = field(init=True)
    Dimensions: list[int] | str = field(init=True)
    Variant: ua.Variant | None = field(init=False, default=None)
    PLC: Any | None = field(init=False, default=None)
    Children: list[Tag] = field(init=False, default_factory=lambda: [])

    def __post_init__(self):
        if isinstance(self.Dimensions, str):
            try:
                dims_list = [int(x) for x in self.Dimensions.split()]
                if 0 in dims_list:
                    self.Dimensions = []
                else:
                    self.Dimensions = dims_list
            except ValueError as e:
                logging.exception(e)
                self.Dimensions = []
        elif not isinstance(self.Dimensions, list):
            raise ValueError(f"Dimensions must be a string or list, got {type(self.Dimensions)}")
        
        self.DataType = sanitizeName(self.DataType)

    def __str__(self):
        return f"{self.Name} ( DataType={self.DataType}, Dimensions={self.Dimensions}, Variant={self.Variant}, Children={self.Children} )"

def createTag(element: Element, Name:str = None, DataType:str = None, Dimensions:str = None) -> Tag:
    if Name is None:
        Name = element.get("Name")
    if DataType is None:
        DataType = element.get("DataType")
    if Dimensions is None:
        Dimensions = element.get("Dimensions", [])

    tag = Tag(Name = Name,
              DataType = DataType,
              Dimensions = Dimensions)

    if not tag.Dimensions:
        v = element.find("./Data[@Format='String']")
        if v is not None:

            value = v.text.strip().removeprefix("'").removesuffix("'")
            tag.Variant = createVariant(value, ua.VariantType.String)
        else:
            data = element.find(".Data[@Format='Decorated']")
            if data:
                element = data
            data = element.find("./Structure")
            if data:
                element = data

            v = element.find("./DataValue")
            if v is not None:
                tag.Variant = createVariant(v.get("Value"), tag.DataType)
            else:
                v = element.get("Value", None)
                if v is not None:
                    v = getUAValue(v, tag.DataType)
                    tag.Variant = createVariant(v, tag.DataType)
                else:
                    dvm = element.findall("./DataValueMember")
                    for member in dvm:
                        tag.Children.append(createTag(member))

                    sm = element.findall("./StructureMember")
                    for member in sm:
                        tag.Children.append(createTag(member))

                    am = element.findall("./ArrayMember")
                    for member in am:
                        tag.Children.append(createTag(member))

                    test = DataTypeRegistry.get(tag.DataType)()

                    tag.Variant = createVariant(test, tag.DataType)
    else:
        data = element.find("./Data")
        if data:
            element = data

        dim = tag.Dimensions

        data = []
        dataData = []
        for e in element.findall("./Array/Element"):
            i = getIndex(e.get("Index"))

            setArray(data, i, getUAValue(e.get("Value"), tag.DataType))
            setArray(dataData, i, DataTypeRegistry.get(tag.DataType)())

            if DataTypeRegistry.has(tag.DataType):
                value = DataTypeRegistry.get(tag.DataType)()
                if isPLCInstance(value, SupportsSetValue):
                    value.setValue(e.get("Value"))
            else:
                value = getUAValue(e.get("Value"), tag.DataType)

        for e in element.findall("./Element"):
            i = getIndex(e.get("Index"))

            s = e.find("./Structure")
            if s:
                DataType = s.get("DataType")
                Dimensions = s.get("Dimensions", [])
                t = createTag(s,
                              Name = i,
                              DataType = DataType,
                              Dimensions = Dimensions)

                v = t.Variant.Value
            else:
                v = getUAValue(e.get("Value"), tag.DataType)

            setArray(data, i, v)
            setArray(dataData, i, DataTypeRegistry.get(tag.DataType)())

            if DataTypeRegistry.has(tag.DataType):
                value = DataTypeRegistry.get(tag.DataType)()
                if isPLCInstance(value, SupportsSetValue):
                    value.setValue(e.get("Value"))
            else:
                value = getUAValue(e.get("Value"), tag.DataType)

        tag.Variant = createVariant(value=data,
                                    variantType=tag.DataType,
                                    dimensions=dim)
        
        tag.PLC = Array[DataTypeRegistry.get(tag.DataType)](DataTypeRegistry.get(tag.DataType), dataData)

    logging.debug(f"createTag, {tag}")
    return tag

def getIndex(index:str) -> list[int]:
    i = index.lstrip("[").rstrip("]").split(",")
    i = list(map(int, i))
    return i

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