import math

from typing import Any

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from engine.errors import MinorFault
from instructions.helper import getPLCValue
from engine.fbd.block import FBDBlock

from datatypes.fdb import FBD_MATH, FBD_MATH_ADVANCED

@InstructionRegistry.register
class ADD(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA + SourceB

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
class ADD__F(ADD):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class SUB(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)        
        return SourceA - SourceB

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
class SUB__F(SUB):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class DIV(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        if SourceB > 0:
            return SourceA / SourceB
        else:
            raise MinorFault(4, 4)

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
class DIV__F(DIV):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)


@InstructionRegistry.register
class MUL(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA * SourceB

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
class MUL__F(MUL):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class MOD(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        if SourceB > 0:
            return SourceA % SourceB
        else:
            raise MinorFault(4, 4)

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
class MOD__F(MOD):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class SQR(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return math.sqrt(Source)

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

@InstructionRegistry.register
class SQR__F(SQR):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class SQRT(SQR):
    pass

@InstructionRegistry.register
class SQRT__F(SQR__F):
    pass


@InstructionRegistry.register
class ABS(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return abs(Source)

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

@InstructionRegistry.register
class ABS__F(ABS):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class NEG(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return 0 - Source

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

@InstructionRegistry.register
class NEG__F(NEG):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class CPT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Dest = self.getMemory(self.args[0])
            Expression = getPLCValue(self.getMemory(self.args[1]))

            Dest.setValue(Expression)