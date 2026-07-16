import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class SIN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.sin(value))
    
@InstructionRegistry.register
class COS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.cos(value))
    
@InstructionRegistry.register
class TAN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.tan(value))
    
@InstructionRegistry.register
class ASN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.asin(value))
    
@InstructionRegistry.register
class ACS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.acos(value))
    
@InstructionRegistry.register
class ATN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], math.atan(value))
    
@InstructionRegistry.register
class ATAN2(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            y_val = self.getMemory(self.args[0], OutputType.PLC)
            x_val = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], math.atan2(y_val, x_val))