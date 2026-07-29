import math

from typing import Any
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue
from engine.fbd.block import FBDBlock

@InstructionRegistry.register
class LN(Instruction):

    def execute(self, Source) -> Any:
        if not isinstance(Source, (int, float)):
            raise NotImplementedError(f"{__class__} not implemented yet")
        if Source <= 0:
            raise NotImplementedError(f"{__class__} not implemented yet")
        return float(math.log(Source))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
            Dest = self.getMemory(self.args[1])

            result = self.execute(Source)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class LOG(Instruction):

    def execute(self, Source) -> Any:
        if not isinstance(Source, (int, float)):
            raise NotImplementedError(f"{__class__} not implemented yet")
        if Source <= 0:
            raise NotImplementedError(f"{__class__} not implemented yet")
        return float(math.log10(Source))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
            Dest = self.getMemory(self.args[1])

            result = self.execute(Source)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class XPY(Instruction):

    def execute(self, SourceX, SourceY) -> Any:
        if not isinstance(SourceX, (int, float)) or not isinstance(SourceY, (int, float)):
            raise NotImplementedError(f"{__class__} not implemented yet")
        return float(math.pow(SourceX, SourceY))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceX = getPLCValue(self.getMemory(self.args[0]))
            SourceY = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])

            result = self.execute(SourceX, SourceY)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceX = block.inParams["SourceX"].Value
        SourceY = block.inParams["SourceY"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceX, SourceY)

@InstructionRegistry.register
class EXPT(XPY):
    pass