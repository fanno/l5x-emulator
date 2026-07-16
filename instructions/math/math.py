import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class ADD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], aValue + bValue)

@InstructionRegistry.register
class SUB(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], aValue - bValue)

@InstructionRegistry.register
class DIV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], aValue / bValue)

@InstructionRegistry.register
class MUL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], aValue * bValue)

@InstructionRegistry.register
class MOD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], aValue % bValue)

@InstructionRegistry.register
class SQR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.sqrt(value))

@InstructionRegistry.register
class ABS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], abs(value))

@InstructionRegistry.register
class NEG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], 0 - value)

@InstructionRegistry.register
class CPT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            result = self.getMemory(self.args[1], OutputType.PLC)
            self.setMemory(self.args[0], result)

@InstructionRegistry.register
class SQRT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")