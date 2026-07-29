import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue
from typing import Any
from engine.fbd.block import FBDBlock


@InstructionRegistry.register
class SIN(Instruction):

    def execute(self, Source) -> Any:
        return math.sin(Source)

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
class COS(Instruction):

    def execute(self, Source) -> Any:
        return math.cos(Source)

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
class TAN(Instruction):

    def execute(self, Source) -> Any:
        return math.tan(Source)

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
class ASN(Instruction):

    def execute(self, Source) -> Any:
        return math.asin(Source)

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
class ASIN(ASN):
    pass

@InstructionRegistry.register
class ACS(Instruction):

    def execute(self, Source) -> Any:
        return math.acos(Source)

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
class ACOS(ACS):
    pass

@InstructionRegistry.register
class ATN(Instruction):

    def execute(self, Source) -> Any:
        return math.atan(Source)

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
class ATAN(ATN):
    pass

@InstructionRegistry.register
class ATAN2(Instruction):

    def execute(self, SourceY, SourceX) -> Any:
        return math.atan2(SourceY, SourceX)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceY = getPLCValue(self.getMemory(self.args[0]))
            SourceX = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])

            result = self.execute(SourceY, SourceX)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceY = block.inParams["SourceY"].Value
        SourceX = block.inParams["SourceX"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceY, SourceX)