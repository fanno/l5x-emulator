from typing import TypeVar, Dict

from asyncua import ua

TT = TypeVar("TT", bound=type)
    
class DataPythonTypesRegistry:
    _Types: Dict[str, ua.VariantType] = {}

    @staticmethod
    def add(name:str) -> None:
        name = name.upper()

        from core.registry.datatyperegistry import DataTypeRegistry
        if DataTypeRegistry.has(name):
            cls = DataTypeRegistry.get(name)()
            if hasattr(cls, "_py_variant"):
                DataPythonTypesRegistry._Types[name] = getattr(cls, "_py_variant")

    @staticmethod
    def getAll() -> Dict[str, ua.VariantType]:
        return DataPythonTypesRegistry._Types
    
    @staticmethod
    def get(name:str) -> ua.VariantType:
        name = name.upper()
        return DataPythonTypesRegistry._Types.get(name, None)

    @staticmethod
    def has(name:str) -> bool:
        name = name.upper()
        return name in DataPythonTypesRegistry._Types