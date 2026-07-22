import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from engine.errors import MinorFault

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class ADD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = getPLCValue(self.getMemory(self.args[0]))
            bValue = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            dest.setValue(aValue + bValue)

@InstructionRegistry.register
class SUB(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = getPLCValue(self.getMemory(self.args[0]))
            bValue = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            dest.setValue(aValue - bValue)

@InstructionRegistry.register
class DIV(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = getPLCValue(self.getMemory(self.args[0]))
            bValue = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            if bValue > 0:
                dest.setValue(aValue / bValue)
            else:
                raise MinorFault(4, 4)

@InstructionRegistry.register
class MUL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = getPLCValue(self.getMemory(self.args[0]))
            bValue = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            dest.setValue(aValue * bValue)

@InstructionRegistry.register
class MOD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = getPLCValue(self.getMemory(self.args[0]))
            bValue = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            if aValue > 0 and bValue > 0:
                dest.setValue(aValue % bValue)
            else:
                raise MinorFault(4, 4)

@InstructionRegistry.register
class SQR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])            

            dest.setValue(math.sqrt(value))
            
@InstructionRegistry.register
class SQRT(SQR):
    pass

@InstructionRegistry.register
class ABS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(abs(value))

@InstructionRegistry.register
class NEG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(0 - value)

@InstructionRegistry.register
class CPT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dest = self.getMemory(self.args[0])
            result = getPLCValue(self.getMemory(self.args[1]))

            dest.setValue(result)
