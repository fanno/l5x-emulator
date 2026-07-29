import math

from typing import Any

from engine.fbd.block import FBDBlock
from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MinorFault

from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

from datatypes.custom.numbers import SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT

@InstructionRegistry.register
class DEG(Instruction):

    def execute(self, Source) -> Any:
        return float(math.degrees(Source))

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
class RAD(Instruction):

    def execute(self, Source) -> Any:
        if not isinstance(Source, (int, float)):
            raise NotImplementedError("Unsupported RAD combination")
        return float(math.radians(Source))

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

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if value < 0:
            raise MinorFault(4, 4)

        result = 0
        shift = 0
        while value > 0:
            result |= (value % 10) << (shift * 4)
            value //= 10
            shift += 1

        if isinstance(dest, (SINT, USINT)):
            if result > 99:
                raise MinorFault(4, 4)
        elif isinstance(dest, (INT,UINT)):
            if result > 9999:
                raise MinorFault(4, 4)
        elif isinstance(dest, (DINT,UDINT)):
            if result > 99999999:
                raise MinorFault(4, 4)
        elif isinstance(dest, (LINT,ULINT)):
            if result > 9999999999999999:
                raise MinorFault(4, 4)

        dest.setValue(result)

@InstructionRegistry.register
class TO_BCD(TOD):
    pass

@InstructionRegistry.register
class FRD(Instruction):

    def execute(self, Source) -> Any:
        if not isinstance(Source, (int, float)):
            raise NotImplementedError("Unsupported FRD combination")

        return float(Source - int(Source))

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
class BCD_TO(FRD):
    pass

@InstructionRegistry.register
class TRN(Instruction):

    def execute(self, Source) -> Any:
        if not isinstance(Source, (int, float)):
            raise NotImplementedError("Unsupported TRN combination")

        if Source >= 0:
            result = int(Source + 0.5)
        else:
            result = int(Source - 0.5)
        return result

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
class TRUNC(TRN):
    pass