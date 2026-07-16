import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class LN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if not isinstance(value, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")
            if value <= 0:
                raise NotImplementedError(f"{__class__} not implemented yet")

            self.setMemory(self.args[1], float(math.log(value)))

@InstructionRegistry.register
class LOG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if not isinstance(value, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")
            if value <= 0:
                raise NotImplementedError(f"{__class__} not implemented yet")

            self.setMemory(self.args[1], float(math.log10(value)))

@InstructionRegistry.register
class XPY(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            x = self.getMemory(self.args[0], OutputType.PLC)
            y = self.getMemory(self.args[1], OutputType.PLC)

            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")

            self.setMemory(self.args[2], float(math.pow(x, y)))