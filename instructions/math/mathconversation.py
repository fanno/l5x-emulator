import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class DEG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported DEG combination")

        self.setMemory(self.args[1], float(math.degrees(value)))

@InstructionRegistry.register
class RAD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported RAD combination")

        self.setMemory(self.args[1], float(math.radians(value)))

@InstructionRegistry.register
class TOD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported TOD combination")

        self.setMemory(self.args[1], int(value))

@InstructionRegistry.register
class FRD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported FRD combination")

        self.setMemory(self.args[1], float(value - int(value)))

@InstructionRegistry.register
class TRN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, (int, float)):
            raise NotImplementedError("Unsupported TRN combination")

        if value >= 0:
            result = int(value + 0.5)
        else:
            result = int(value - 0.5)

        self.setMemory(self.args[1], result)
    
@InstructionRegistry.register
class TRUNC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")