import logging

from typing import TypeVar, Dict, Type, ClassVar

from opcua.structure import sanitizeName

T = TypeVar("T", bound=type)

class DataTypeRegistry:
    _global_registry: ClassVar[Dict[str, Type]] = {}
    _local_registry: ClassVar[Dict[str, Type]] = {}

    @staticmethod
    def register(cls: T) -> T:
        # ADD THIS CHECK:
        if isinstance(cls, list):
            raise TypeError(f"Cannot register a list! Got: {cls}")

        name = cls.__name__
        if name is not None:
            name = name.upper()
            if name in DataTypeRegistry._global_registry:
                raise RuntimeError(f"DataType global, {name} already registered")
            logging.debug(f"{name}")
            DataTypeRegistry._global_registry[name] = cls

            from core.registry.datauatypesregistry import DataUATypesRegistry
            DataUATypesRegistry.add(name)
            from core.registry.datapythontypesregistry import DataPythonTypesRegistry
            DataPythonTypesRegistry.add(name)
        return cls

    @staticmethod
    def register_local(cls: T) -> T:
        if isinstance(cls, list):
            raise TypeError(f"Cannot register a list! Got: {cls}")

        name = cls.__name__
        if name is not None:
            name = name.upper()
            if name in DataTypeRegistry._local_registry:
                raise RuntimeError(f"DataType local, {name} already registered")
            logging.debug(f"{name}")
            DataTypeRegistry._local_registry[name] = cls

            from core.registry.datauatypesregistry import DataUATypesRegistry
            DataUATypesRegistry.add(name)
            from core.registry.datapythontypesregistry import DataPythonTypesRegistry
            DataPythonTypesRegistry.add(name)
        return cls    

    @staticmethod
    def getAll() -> Dict[str, Type]:
        return {**DataTypeRegistry._global_registry, **DataTypeRegistry._local_registry}

    @staticmethod
    def get(name:str) -> Type:
        name = sanitizeName(name)
        if name in DataTypeRegistry._global_registry:
            return DataTypeRegistry._global_registry[name]
        if name in DataTypeRegistry._local_registry:
            return DataTypeRegistry._local_registry[name]
        raise KeyError(f"DataType {name} not found")
    
    @staticmethod
    def has(name:str) -> bool:
        name = sanitizeName(name)
        return name in DataTypeRegistry._global_registry or name in DataTypeRegistry._local_registry
    
    @staticmethod
    def clear_local() -> None:
        DataTypeRegistry._local_registry = {}