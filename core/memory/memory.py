from typing import Dict, Any, Type
from dataclasses import dataclass, field

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array

@dataclass
class Memory:
    NAME:str = field(init=True)
    _memory: Dict[str, Type] = field(init=False, default_factory=dict)
    _changed: Dict[str, bool] = field(init=False, default_factory=dict)

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
        from core.memory.helper import resolvePath, isBitIndex, resolveKey
        keys:list[str|int] = resolvePath(keys)

        if isBitIndex(keys):
            container = self.__getContainer(keys[:-2])
            key = resolveKey(container, keys[-2])

            bit_index = int(keys[-1])
            bit_value = int(v) & 1

            mask = 1 << bit_index

            if isinstance(container, (dict, list, Array)):
                value = container[key]
            else:
                value = getattr(container, key)

            if isinstance(value, DataVariant):
                value = value.getPLCValue()

            new_int = (value & ~mask) | (bit_value << bit_index)

            self.__set(container, key, new_int, rawValue)
        else:
            container = self.__getContainer(keys[:-1])
            key = resolveKey(container, keys[-1])
            self.__set(container, key, v, rawValue)

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

        if isinstance(current, DataVariant):
            if isinstance(newValue, DataVariant):
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
        from core.memory.helper import resolvePath, isBitIndex, isBitSet, getValue
        keys:list[str|int] = resolvePath(keys)

        if isBitIndex(keys):
            container = self.__getContainer(keys[:-2])
            value = getValue(container, keys[-2])
            if isinstance(value, DataVariant):
                value = value.getPLCValue()
            return isBitSet(value, int(keys[-1]))
        else:
            container = self.__getContainer(keys[:-1])
            return getValue(container, keys[-1])

    def has(self, keys:str|list|tuple) -> bool:
        from core.memory.helper import resolvePath, isBitIndex, resolveKey
        keys:list[str|int] = resolvePath(keys)

        try:
            if isBitIndex(keys):
                container = self.__getContainer(keys[:-2])
                leaf_key = keys[-2]
            else:
                container = self.__getContainer(keys[:-1])
                leaf_key = keys[-1]

            leaf_key = resolveKey(container, leaf_key)
            if isinstance(container, dict):
                return leaf_key in container
            if isinstance(container, (list, Array)):
                return (0 <= leaf_key and leaf_key < len(container))
            else:
                return hasattr(container, leaf_key)
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
    