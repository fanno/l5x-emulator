import logging

from typing import TypeVar, Dict, Type, ClassVar

from opcua.structure import sanitizeName

T = TypeVar("T", bound=type)

class DataTypeRegistry:
    _registry: ClassVar[Dict[str, Type]] = {}

    @staticmethod
    def register(cls: T) -> T:
        # ADD THIS CHECK:
        if isinstance(cls, list):
            raise TypeError(f"Cannot register a list! Got: {cls}")

        logging.debug(f"DataTypeRegistry.register: {cls}")
        name = cls.__name__
        if name is not None:
            name = name.upper()
            if name in DataTypeRegistry._registry:
                raise RuntimeError(f"DataType {name} already registered")
            logging.debug(f"{name}")
            DataTypeRegistry._registry[name] = cls

            from core.registry.datauatypesregistry import DataUATypesRegistry
            DataUATypesRegistry.add(name)
            from core.registry.datapythontypesregistry import DataPythonTypesRegistry
            DataPythonTypesRegistry.add(name)
        return cls

    @staticmethod
    def getAll() -> Dict[str, Type]:
        return DataTypeRegistry._registry

    @staticmethod
    def get(name:str) -> Type:
        name = sanitizeName(name)
        return DataTypeRegistry._registry[name]
    
    @staticmethod
    def has(name:str) -> bool:
        name = sanitizeName(name)
        return name in DataTypeRegistry._registry