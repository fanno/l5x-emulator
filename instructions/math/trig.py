import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue
from typing import Any
from engine.fbd.block import FBDBlock

from datatypes.fdb import FBD_MATH_ADVANCED


@InstructionRegistry.register
class SIN(Instruction):

    def execute(self, Source) -> Any:
        return math.sin(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class SIN__F(SIN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)
    
@InstructionRegistry.register
class COS(Instruction):

    def execute(self, Source) -> Any:
        return math.cos(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class COS__F(COS):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)        
    
@InstructionRegistry.register
class TAN(Instruction):

    def execute(self, Source) -> Any:
        return math.tan(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class TAN__F(TAN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ASN(Instruction):

    def execute(self, Source) -> Any:
        return math.asin(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class ASN__F(ASN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)
    
@InstructionRegistry.register
class ASIN(ASN):
    pass

@InstructionRegistry.register
class ASIN__F(ASN__F):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ACS(Instruction):

    def execute(self, Source) -> Any:
        return math.acos(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class ACS__F(ACS):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ACOS(ACS):
    pass

@InstructionRegistry.register
class ACOS__F(ACS__F):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ATN(Instruction):

    def execute(self, Source) -> Any:
        return math.atan(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = getPLCValue(self.getMemory(self.args[0]))
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
class ATN__F(ATN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ATAN(ATN):
    pass

@InstructionRegistry.register
class ATAN__F(ATN__F):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class ATAN2(Instruction):

    def execute(self, SourceY, SourceX) -> Any:
        return math.atan2(SourceY, SourceX)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            SourceY = getPLCValue(self.getMemory(self.args[0]))
            SourceX = getPLCValue(self.getMemory(self.args[1]))
            Dest = self.getMemory(self.args[2])

            result = self.execute(SourceY, SourceX)
            Dest.setValue(result)

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        SourceY = self.getMemory(self.args[0])
        SourceX = self.getMemory(self.args[1])
        return self.execute(SourceY, SourceX)

@InstructionRegistry.register
class ATAN2__F(ATAN2):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceY = block.inParams["SourceY"].Value
        SourceX = block.inParams["SourceX"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceY, SourceX)
