import math

from typing import Any
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue
from engine.fbd.block import FBDBlock

from datatypes.fdb import FBD_MATH, FBD_MATH_ADVANCED

@InstructionRegistry.register
class LN(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        if Source <= 0:
            return 0.0
        return float(math.log(Source))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = self.getMemory(self.args[0])
            Dest = self.getMemory(self.args[1])

            result = self.execute(Source)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        math:FBD_MATH_ADVANCED = block.Value
        if math.EnableIn:
            math.Dest.setValue(self.execute(math.Source))
        math.EnableOut.setValue(math.EnableIn)

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        Source = self.getMemory(self.args[0])
        return self.execute(Source)        

@InstructionRegistry.register
class LN__F(LN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class LOG(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        if Source <= 0:
            return 0.0
        return float(math.log10(Source))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = self.getMemory(self.args[0])
            Dest = self.getMemory(self.args[1])

            result = self.execute(Source)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        math:FBD_MATH_ADVANCED = block.Value
        if math.EnableIn:
            math.Dest.setValue(self.execute(math.Source))
        math.EnableOut.setValue(math.EnableIn)

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        Source = self.getMemory(self.args[0])
        return self.execute(Source)

@InstructionRegistry.register
class LOG__F(LOG):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class XPY(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return float(math.pow(SourceA, SourceB))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            Dest = self.getMemory(self.args[2])

            result = self.execute(SourceA, SourceB)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        math:FBD_MATH = block.Value
        if math.EnableIn:
            math.Dest.setValue(self.execute(math.SourceA, math.SourceB))
        math.EnableOut.setValue(math.EnableIn)

@InstructionRegistry.register
class XPY__F(XPY):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class EXPT(XPY):
    pass

@InstructionRegistry.register
class EXPT__F(XPY__F):
    pass