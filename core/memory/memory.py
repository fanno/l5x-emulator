from enum import Enum
from typing import Dict, Any, Type
from dataclasses import dataclass, field

from datatypes.custom.array import Array

from datatypes.custom.numbers import INTIGER
from datatypes.custom.udt import UDT

from lxml.etree import _Element as Element

from protocols.memory import SupportsGetPLCValue, SupportsSetValue
from utils.isplcinstance import isPLCInstance

class OpcUaAccess(Enum):
    NONE = "None"
    READ = "Read Only"
    READ_WRITE = "Read/Write"

    @classmethod
    def from_string(cls, value: str | None) -> "OpcUaAccess":
        if value is None:
            return cls.NONE

        #value = value.upper()

        if value == "Read Only":
            return cls.READ

        if value == "Read/Write":
            return cls.READ_WRITE

        return cls.NONE

@dataclass
class TagMetadata:
    OpcUa_Access: OpcUaAccess = field(init=True, default=OpcUaAccess.NONE)
    XMlElement: Element = field(init=True, default=None)

@dataclass
class Memory:
    NAME:str = field(init=True)
    _memory: Dict[str, Type] = field(init=False, default_factory=dict)
    _changed: Dict[str, bool] = field(init=False, default_factory=dict)
    _metadata: Dict[str, TagMetadata] = field(init=False, default_factory=dict)

    def __getContainer(self, keys):
        from core.memory.helper import resolveKey

        container = self._memory
        for key in keys:
            key = resolveKey(container, key)
            if isinstance(container, dict):
                if key in container:
                    container = container.get(key)
                else:
                    raise AttributeError(F"{keys}, {key}")
            elif isinstance(container, (list, Array)):
                if not isinstance(key, int):
                    key = int(key)
                container = container[key]
            else:
                if hasattr(container, key):
                    container = getattr(container, key)
                else:
                    raise AttributeError(F"{keys}, {key}")
        return container

    def set(self, keys:str|list|tuple, v:Type, rawValue:bool=False) -> None:
        from core.memory.helper import resolvePath, resolveKey
        keys:list[str|int] = resolvePath(keys)

        lastKey = keys[-1]
        if isinstance(lastKey, int):
            container = self.__getContainer(keys[:-1])
            if isinstance(container, INTIGER):
                bit = container[lastKey]
                bit.setValue(v)
                return
            
        container = self.__getContainer(keys[:-1])
        key = resolveKey(container, lastKey)
        self.__set(container, key, v, rawValue)
        return

    def __set(self, container, key, newValue, rawValue:bool=False):
        if rawValue:
            self.__assign(container, key, newValue)
            return
        
        current = None
        if isinstance(container, (dict, list, Array)):
            if key in container:
                current = container[key]
        elif hasattr(container, key):
            current = getattr(container, key)

        if isPLCInstance(current, SupportsSetValue):
            if isPLCInstance(newValue, SupportsGetPLCValue):
                current.setValue(newValue.getPLCValue())
            else:
                current.setValue(newValue)
            return
        
        self.__assign(container, key, newValue)
        
    @staticmethod
    def __assign(container, key, value):
        if isinstance(container, (dict, list, Array)):
            container[key] = value
        else:
            setattr(container, key, value)

    def get(self, keys:str|list|tuple) -> Any:
        from core.memory.helper import resolvePath, resolveKey
        keys:list[str|int] = resolvePath(keys)

        lastKey = keys[-1]
        if isinstance(lastKey, int):
            container = self.__getContainer(keys[:-1])
            if isinstance(container, INTIGER):
                return container[lastKey]

        container = self.__getContainer(keys[:-1])
        key = resolveKey(container, lastKey)
        return self._get(container, key)

    def _get(self, container:dict|list|int, key:str|int) -> Any:
        from core.memory.helper import resolveKey
        key = resolveKey(container, key)
        if isinstance(container, dict):
            if key is None or key not in container:
                raise KeyError(f"Missing dict key: {key} {container}")
            return container[key]
        elif isinstance(container, UDT):
            if not hasattr(container, key):
                raise KeyError(f"Missing UDT key: {key} {container}")
            return getattr(container, key)
        elif isinstance(container, (list, Array)):
            if key is None:
                raise IndexError("Leaf key is None for list access")
            return container[key]
        else:
            if key is None or not hasattr(container, key):
                raise AttributeError(f"Missing attribute: {key} {container}")
            return getattr(container, key)

    def has(self, keys:str|list|tuple) -> bool:
        from core.memory.helper import resolvePath, resolveKey
        keys:list[str|int] = resolvePath(keys)

        try:
            lastKey = keys[-1]
            container = self.__getContainer(keys[:-1])
            if isinstance(lastKey, int):
                if isinstance(container, INTIGER):
                    return True

            key = resolveKey(container, lastKey)
            if isinstance(container, dict):
                return key in container
            if isinstance(container, (list, Array)):
                return (0 <= key and key < len(container))
            else:
                return hasattr(container, key)
        except Exception:
            return False
    
    def needMemoryUpdate(self, keys:str|list|tuple) -> bool:
        from core.memory.helper import resolvePath, getHash
        result:bool = False

        keys = resolvePath(keys)
        if self.has(keys):
            key:str = ".".join(keys)
            currentHash = getHash(self.get(keys))

            oldHash = self._changed.get(key, None)
            if oldHash is not None:
                result = oldHash != currentHash
            else:
                result = True

            self._changed[key] = currentHash
        return result

    def getMemoryAll(self) -> Dict[str, Type]:
        return self._memory

    def size(self) -> int:
        return len(self._memory)

    def set_metadata(self, keys: str | list | tuple, metadata: TagMetadata ) -> None:
        from core.memory.helper import resolvePath
        keys = resolvePath(keys)
        key = ".".join(str(k) for k in keys)
        self._metadata[key] = metadata

    def get_metadata(self, keys: str | list | tuple) -> TagMetadata | None:
        from core.memory.helper import resolvePath
        keys = resolvePath(keys)
        key = ".".join(str(k) for k in keys)

        return self._metadata.get(key)

class PlcMemory:
    _container: Dict[str, Memory] = {}

    @staticmethod
    def addContainer(container:Memory) -> None:
        PlcMemory._container[container.NAME] = container

    @staticmethod
    def getContainer(name:str) -> Memory | None:
        if name in PlcMemory._container:
            return PlcMemory._container[name]
        return None

    @staticmethod
    def getContainers() -> Dict[str, Memory]:
        return PlcMemory._container