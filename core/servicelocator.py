from typing import TypeVar, Dict, Optional, Type

T = TypeVar('T')

class ServiceLocator:
    _services: Dict[str, object] = {}
    
    @classmethod
    def register(cls, service: object, name: Optional[str] = None) -> None:
        key = name if name else type(service).__name__
        
        if key in cls._services:
            raise ValueError(
                f"Service '{key}' is already registered. "
                f"Use 'set()' to overwrite or choose a different name."
            )
        
        cls.set(service, name)
    
    @classmethod
    def get(cls, expected_type: Type[T], name: Optional[str] = None) -> T:
        key = name if name else expected_type.__name__
        service = cls._services.get(key)
        
        if service is None:
            raise KeyError(f"Service '{key}' not registered")
        if not isinstance(service, expected_type):
            raise TypeError(
                f"Service '{key}' is {type(service).__name__}, expected {expected_type.__name__}"
            )
        return service
    
    @classmethod
    def set(cls, service: object, name: Optional[str] = None) -> None:
        key = name if name else type(service).__name__
        cls._services[key] = service

    @classmethod
    def unregister(cls, name: str) -> None:
        cls._services.pop(name, None)
    
    @classmethod
    def reset(cls) -> None:
        cls._services.clear()