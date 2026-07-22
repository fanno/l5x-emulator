import engine.context
from typing import Any
from core.memory.helper import OutputType
from core.memory.memory import Memory

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

class Instruction:
    args:list[str]
    name:str
    memory:Memory

    def __init__(self, name:str = None, args:list[str] = None, memory:Memory = None):
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name
        if args is None:
            self.args = []
        else:
            self.args = args
        self._memory = memory

    def getMemory(self, path:list[str] | str) -> DataVariant|Array|UDT:
        if self._memory is None:
            from core.memory.helper import getMemory
            return getMemory(path)
        else:
            return self._memory.get(path)
    
    def setMemory(self, path:list[str] | str, value):
        if self._memory is None:
            from core.memory.helper import setMemory
            setMemory(path, value)
        else:
            self._memory.set(path)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass
    
    async def postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass    