import math

from typing import Any

from engine.fbd.block import FBDBlock
from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MinorFault

from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

from datatypes.custom.numbers import SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT
from datatypes.fdb import FBD_CONVERT, FBD_MATH_ADVANCED, FBD_CONVERT

@InstructionRegistry.register
class DEG(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return float(math.degrees(Source))

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
class DEG__F(DEG):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class RAD(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return float(math.radians(Source))

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
class RAD__F(RAD):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

def to_bcd(value: int) -> int:
    bcd = 0
    shift = 0
    while value > 0:
        bcd |= (value % 10) << (shift * 4)
        value //= 10
        shift += 1
    return bcd

@InstructionRegistry.register
class TOD(Instruction):

    def execute(self, Source, Dest)-> Any:
        if Source < 0:
            raise MinorFault(4, 4)

        result = 0
        shift = 0
        while Source > 0:
            result |= (Source % 10) << (shift * 4)
            Source //= 10
            shift += 1

        if isinstance(Dest, (SINT, USINT)):
            if result > 99:
                raise MinorFault(4, 4)
        elif isinstance(Dest, (INT,UINT)):
            if result > 9999:
                raise MinorFault(4, 4)
        elif isinstance(Dest, (DINT,UDINT)):
            if result > 99999999:
                raise MinorFault(4, 4)
        elif isinstance(Dest, (LINT,ULINT)):
            if result > 9999999999999999:
                raise MinorFault(4, 4)

        return result

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        Source = self.getMemory(self.args[0])
        Dest = self.getMemory(self.args[1])

        result = self.execute(Source, Dest)

        Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        value:FBD_CONVERT = block.Value
        if value.EnableIn:
            result = self.execute(value.Source, value.Dest)
            value.Dest.setValue(result)
        value.EnableOut.setValue(value.EnableIn)

@InstructionRegistry.register
class TO_BCD(TOD):
    pass

@InstructionRegistry.register
class FRD(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return float(Source - int(Source))

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = self.getMemory(self.args[0])
            Dest = self.getMemory(self.args[1])
            
            result = self.execute(Source)
            Dest.setValue(result)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        math:FBD_CONVERT = block.Value

        if math.EnableIn:
            math.Dest.setValue(self.execute(math.Source))
        math.EnableOut.setValue(math.EnableIn)

@InstructionRegistry.register
class BCD_TO(FRD):
    pass

@InstructionRegistry.register
class TRN(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        if Source >= 0:
            result = int(Source + 0.5)
        else:
            result = int(Source - 0.5)
        return result

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
class TRN__F(TRN):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)

@InstructionRegistry.register
class TRUNC(TRN):
    pass

@InstructionRegistry.register
class TRUNC__F(TRN__F):
    pass