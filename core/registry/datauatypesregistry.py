from typing import TypeVar, Dict

from asyncua import ua

TT = TypeVar("TT", bound=type)
    
class DataUATypesRegistry:
    _Types: Dict[str, ua.VariantType] = {}

    @staticmethod
    def add(name:str) -> None:
        name = name.upper()
        from core.registry.datatyperegistry import DataTypeRegistry
        if DataTypeRegistry.has(name):
            cls = DataTypeRegistry.get(name)

            instance = cls()
            
            if hasattr(instance, "_ua_variant"):
                DataUATypesRegistry._Types[name] = getattr(instance, "_ua_variant")
            else:
                DataUATypesRegistry._Types[name] = ua.VariantType.ExtensionObject

    @staticmethod
    def getAll() -> Dict[str, ua.VariantType]:
        return DataUATypesRegistry._Types
    
    @staticmethod
    def get(name:str) -> ua.VariantType:
        name = name.upper()
        return DataUATypesRegistry._Types.get(name, ua.VariantType.Null)

    @staticmethod
    def has(name:str) -> bool:
        name = name.upper()
        return name in DataUATypesRegistry._Types