import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class SIN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.sin(value))
    
@InstructionRegistry.register
class COS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.cos(value))
    
@InstructionRegistry.register
class TAN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.tan(value))
    
@InstructionRegistry.register
class ASN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.asin(value))
    
@InstructionRegistry.register
class ASIN(ASN):
    pass

@InstructionRegistry.register
class ACS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.acos(value))
    
@InstructionRegistry.register
class ACOS(ACS):
    pass

@InstructionRegistry.register
class ATN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(math.atan(value))
    
@InstructionRegistry.register
class ATAN(ATN):
    pass

@InstructionRegistry.register
class ATAN2(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            y = getPLCValue(self.getMemory(self.args[0]))
            x = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            dest.setValue(math.atan2(y, x))