import math
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from engine.st.helper import hook_expression



@InstructionRegistry.register
class CMP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            expression = "return " + hook_expression(self.args[0])

            from engine.st.hooks import run_exec_env
            ctx.RungStatus = await run_exec_env(expression, ctx, "CMP")

@InstructionRegistry.register
class LIM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            Value = self.getMemory(self.args[1])
            bValue = self.getMemory(self.args[2])
            
            if aValue < bValue:
                if aValue <= Value or bValue >= Value:
                    ctx.RungStatus = False
            else:
                if aValue >= Value or bValue <= Value:
                    ctx.RungStatus = False

@InstructionRegistry.register
class LIMIT(LIM):
    pass

@InstructionRegistry.register
class MEQ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0])
            maskValue = self.getMemory(self.args[1])
            compageValue = self.getMemory(self.args[2])

            ctx.RungStatus = (sourceValue & maskValue) == (compageValue & maskValue)

@InstructionRegistry.register
class EQU(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])
            
            if aValue != bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class EQ(EQU):
    pass

@InstructionRegistry.register
class NEQ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])
            
            if aValue == bValue:
                ctx.RungStatus = False
                
@InstructionRegistry.register
class NQ(NEQ):
    pass

@InstructionRegistry.register
class LES(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])
            
            if aValue >= bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class LT(LES):
    pass

@InstructionRegistry.register
class GRT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])

            if aValue <= bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class GT(GRT):
    pass

@InstructionRegistry.register
class LEQ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])
            
            if aValue > bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class LE(LEQ):
    pass

@InstructionRegistry.register
class GEQ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            bValue = self.getMemory(self.args[1])
            
            if aValue < bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class GE(GEQ):
    pass

@InstructionRegistry.register
class IsINF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            ctx.RungStatus = math.isinf(source)

@InstructionRegistry.register
class IsNAN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            ctx.RungStatus = math.isnan(source)