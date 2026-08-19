from typing import Any

from core.memory.memory import Memory

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

import engine.context
from engine.fbd.block import FBDBlock
from engine.scan import PreScan, PostScan

from instructions.helper import getOperand

class Instruction:
    args:list[str]
    name:str
    memory:Memory

    block:FBDBlock

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
        self.wires = []

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

    async def ladder(self, ctx:"engine.context.ExecutionContext") -> None:
        emulator = engine.context.EmulatorContext.get()

        if emulator.preScan:
            with PreScan.scope(emulator):
                await self.ladder_preScan(ctx)
        elif emulator.postScan:
            with PostScan.scope(emulator):
                await self.ladder_postScan(ctx)
        else:
            await self.ladder_execute(ctx)

    async def ladder_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

    async def ladder_preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass
    
    async def ladder_postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        pass

    async def fbd(self, ctx:"engine.context.ExecutionContext", block:FBDBlock) -> None:
        value:UDT = getOperand(block)

        emulator = engine.context.EmulatorContext.get()
        if emulator.preScan:
            with PreScan.scope(emulator):
                await self.fbd_preScan(ctx, block)
        elif emulator.postScan:
            with PostScan.scope(emulator):
                await self.fbd_postScan(ctx, block)
        else:
            await self.fbd_execute(ctx, block)

        if value:
            for name, parm in block.outParams.items():
                if hasattr(value, name):
                    parm.Value = getattr(value, name)

    async def fbd_execute(self, ctx:"engine.context.ExecutionContext", block:FBDBlock) -> None:
        self.execute(block.Value, ctx)

    async def fbd_preScan(self, ctx:"engine.context.ExecutionContext", block:FBDBlock) -> None:
        self.preScan(block.Value, ctx)
    
    async def fbd_postScan(self, ctx:"engine.context.ExecutionContext", block:FBDBlock) -> None:
        self.postScan(block.Value, ctx)

    async def sfc(self, ctx:"engine.context.ExecutionContext") -> None:
        emulator = engine.context.EmulatorContext.get()
        if emulator.preScan:
            with PreScan.scope(emulator):
                await self.sfc_preScan(ctx)
        elif emulator.postScan:
            with PostScan.scope(emulator):
                await self.sfc_postScan(ctx)
        else:
            await self.sfc_execute(ctx)

    async def st(self, ctx:"engine.context.ExecutionContext") -> None:
        emulator = engine.context.EmulatorContext.get()
        if emulator.preScan:
            with PreScan.scope(emulator):
                await self.st_preScan(ctx)
        elif emulator.postScan:
            with PostScan.scope(emulator):
                await self.st_postScan(ctx)
        else:
            return await self.st_execute(ctx)

    async def st_execute(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_execute(ctx)

    async def st_preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_preScan(ctx)
    
    async def st_postScan(self, ctx:"engine.context.ExecutionContext") -> None:
        await self.ladder_postScan(ctx)

    def postScan(self, udt:UDT, ctx:"engine.context.ExecutionContext") -> None:
        pass

    def preScan(self, udt:UDT, ctx:"engine.context.ExecutionContext") -> None:
        pass

    def execute(self, udt:UDT, ctx:"engine.context.ExecutionContext") -> Any:
        self.raiseNotImplementedError(ctx)

    def raiseNotImplementedError(self, ctx:"engine.context.ExecutionContext"):
        raise NotImplementedError(f"{self.name}, ARGS: {self.args} not implemented yet")
