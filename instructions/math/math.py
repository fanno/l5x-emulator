import math

from typing import Any

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from engine.errors import MinorFault
from instructions.helper import getPLCValue
from engine.fbd.block import FBDBlock

@InstructionRegistry.register
class ADD(Instruction):

    def execute(self, aValue, bValue) -> Any:
        return aValue + bValue

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = getPLCValue(self.getMemory(self.args[0]))
            SourceB = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])
            
            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class SUB(Instruction):

    def execute(self, aValue, bValue) -> Any:
        return aValue - bValue

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = getPLCValue(self.getMemory(self.args[0]))
            SourceB = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])
            
            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class DIV(Instruction):

    def execute(self, aValue, bValue) -> Any:
        if bValue > 0:
            return aValue / bValue
        else:
            raise MinorFault(4, 4)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = getPLCValue(self.getMemory(self.args[0]))
            SourceB = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])
            
            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class MUL(Instruction):

    def execute(self, aValue, bValue) -> Any:
        return aValue * bValue

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = getPLCValue(self.getMemory(self.args[0]))
            SourceB = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])
            
            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class MOD(Instruction):

    def execute(self, aValue, bValue) -> Any:
        if bValue > 0:
            return aValue % bValue
        else:
            raise MinorFault(4, 4)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = getPLCValue(self.getMemory(self.args[0]))
            SourceB = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])
            
            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class SQR(Instruction):

    def execute(self, Source) -> Any:
        return math.sqrt(Source)

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
class SQRT(SQR):
    pass

@InstructionRegistry.register
class ABS(Instruction):

    def execute(self, Source) -> Any:
        return abs(Source)

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
class NEG(Instruction):

    def execute(self, Source) -> Any:
        return 0 - Source

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
class CPT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Dest = self.getMemory(self.args[0])
            Expression = getPLCValue(self.getMemory(self.args[1]))

            Dest.setValue(Expression)