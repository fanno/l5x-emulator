import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MinorFault

from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

from datatypes.custom.numbers import SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT

@InstructionRegistry.register
class DEG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported DEG combination")

        dest.setValue(float(math.degrees(value)))

@InstructionRegistry.register
class RAD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported RAD combination")

        dest.setValue(float(math.radians(value)))

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

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported FRD combination")

        dest.setValue(float(value - int(value)))

@InstructionRegistry.register
class BCD_TO(FRD):
    pass

@InstructionRegistry.register
class TRN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported TRN combination")

        if value >= 0:
            result = int(value + 0.5)
        else:
            result = int(value - 0.5)

        dest.setValue(result)
    
@InstructionRegistry.register
class TRUNC(TRN):
    pass