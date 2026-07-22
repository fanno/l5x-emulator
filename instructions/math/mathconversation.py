import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class DEG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported DEG combination")

        dest.setValue(float(math.degrees(value)))

@InstructionRegistry.register
class RAD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported RAD combination")

        dest.setValue(float(math.radians(value)))

@InstructionRegistry.register
class TOD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = getPLCValue(self.getMemory(self.args[0]))
        dest = self.getMemory(self.args[1])

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported TOD combination")

        dest.setValue(int(value))

@InstructionRegistry.register
class TO_BCD(TOD):
    pass

@InstructionRegistry.register
class FRD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
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

    async def execute(self, ctx:"ExecutionContext") -> None:
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