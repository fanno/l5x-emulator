import engine.context
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

    async def ladder_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

    async def ladder_preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass
    
    async def ladder_postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass

    async def fbd_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_execute(ctx)

    async def fbd_preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_preScan(ctx)
    
    async def fbd_postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_postScan(ctx)

    async def sfc_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.ladder_execute(ctx)
    
    async def sfc_preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_preScan(ctx)
    
    async def sfc_postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_postScan(ctx)

    async def st_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_execute(ctx)


    '''
    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        match ctx.Type:
            case RoutineType.RLL:
                await self.ladder_execute(ctx)
            case RoutineType.FBD:
                await self.fbd_execute(ctx)
            case RoutineType.SFC:
                await self.sfc_execute(ctx)
    
    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        match ctx.Type:
            case RoutineType.RLL:
                await self.ladder_preScan(ctx)
            case RoutineType.FBD:
                await self.fbd_preScan(ctx)
            case RoutineType.SFC:
                await self.sfc_preScan(ctx)
    
    async def postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        match ctx.Type:
            case RoutineType.RLL:
                await self.ladder_postScan(ctx)
            case RoutineType.FBD:
                await self.fbd_postScan(ctx)
            case RoutineType.SFC:
                await self.sfc_postScan(ctx)
    '''