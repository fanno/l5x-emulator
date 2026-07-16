import logging

from typing import Mapping, Type, Dict

from dataclasses import make_dataclass, field, fields, dataclass

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from opcua.structure import Structure
from opcua.helpers import getUAVariantType, getPythonVariantType

from datatypes.custom.array import Array
from datatypes.custom.datavariant import DataVariant

class UDTBase:
    def __repr__(self):
        values = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"

@dataclass()
class UAInfo:
    name: str = field()
    dataType: str = field()
    ua: Type = field()
    dim: list  = field(default_factory=list)

def is_immutable(tp):
    immutable_builtins = (int, float, str, bool, bytes, tuple, frozenset, type(None))
    if tp in immutable_builtins:
        return True
    if hasattr(tp, "__dataclass_fields__"):
        return getattr(tp, "__dataclass_params__").frozen
    return False

def get_ua_info(cls) -> Dict[str, UAInfo]:
    info = {}
    for f in fields(cls):
        if f.repr:
            obj = f.default_factory()
            dataType = f.default_factory.__name__

            if isinstance(obj, DataVariant):
                uatype = obj._ua_variant
            else:
                uatype = ua.VariantType.ExtensionObject

            dim = []
            if isinstance(obj, Array):
                dim = obj.getDim()

            info[f.name] = UAInfo(name=f.name, dataType=dataType, ua=uatype, dim=dim)
    return info

def createClassFromStructure(struct:Structure) -> Type:
    schema = []

    def generate_nested_list(dims, default_val):
        if not dims:
            return default_val
        return [generate_nested_list(dims[1:], default_val) for _ in range(dims[0])]

    for f in struct.fields:
        py_type = getPythonVariantType(f.dataType)

        if f.dimension:
            dim_copy = f.dimension
            val_copy = py_type()

            dv = generate_nested_list(dim_copy, val_copy)

            scalar_default = lambda pt=py_type, d=dv: Array[pt](pt, d)
        else:
            scalar_default = py_type

        _field = field(
            init=False,
            repr=True,
            default_factory=scalar_default
        )

        schema.append((f.name, py_type, _field))

    if struct.base:
        bases = struct.base
    else:
        bases = ()

    cls = create_ua_class(struct.name, schema, bases)
    logging.debug(f"createClassFromStructure: {struct.name} {cls}")
    return cls

def create_ua_class(class_name: str, field_definitions: list[tuple], bases:tuple=()):
    fields = []
    for name, py_type, field in field_definitions:
        fields.append((name, py_type, field))

    return make_dataclass(class_name,
                          fields,
                          bases=bases)

class DataTypes:
    _dataTypes: Mapping[str, Structure] = {}

    @staticmethod
    def add(struct:Structure) -> None:
        if not DataTypes.has(struct.name):
            DataTypes._dataTypes[struct.name] = struct

        if not DataTypeRegistry.has(struct.name):
            DataTypeRegistry.register(createClassFromStructure(struct))

    @staticmethod
    def getAll() -> Mapping[str, Structure]:
        return DataTypes._dataTypes
    
    @staticmethod
    def get(name:str) -> Structure:
        name = name.upper()
        return DataTypes._dataTypes[name]

    @staticmethod
    def has(name:str) -> bool:
        name = name.upper()
        return name in DataTypes._dataTypes