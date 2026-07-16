import math
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from engine.expressionevaluator import ExpressionEvaluator
from engine.st.helper import hook_expression
from engine.errors import STException

from datatypes.custom.datavariant import DataVariant

@InstructionRegistry.register
class CMP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            expression = "return " + hook_expression(self.args[0])

            from engine.st.hooks import run_exec_env
            #expression = make_async_st(expression)
            ctx.RungStatus = await run_exec_env(expression, ctx, "CMP")

@InstructionRegistry.register
class LIM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            Value = self.getMemory(self.args[1], OutputType.PLC)
            bValue = self.getMemory(self.args[2], OutputType.PLC)
            
            if aValue < bValue:
                if aValue <= Value or bValue >= Value:
                    ctx.RungStatus = False
            else:
                if aValue >= Value or bValue <= Value:
                    ctx.RungStatus = False

@InstructionRegistry.register
class MEQ(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0], OutputType.PLC)
            maskValue = self.getMemory(self.args[1], OutputType.PLC)
            compageValue = self.getMemory(self.args[2], OutputType.PLC)

            ctx.RungStatus = (sourceValue & maskValue) == (compageValue & maskValue)

@InstructionRegistry.register
class EQU(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)
            
            if aValue != bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class NEQ(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)
            
            if aValue == bValue:
                ctx.RungStatus = False                

@InstructionRegistry.register
class LES(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)
            
            if aValue >= bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class GRT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)

            if aValue <= bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class LEQ(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)
            
            if aValue > bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class GEQ(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0], OutputType.PLC)
            bValue = self.getMemory(self.args[1], OutputType.PLC)
            
            if aValue < bValue:
                ctx.RungStatus = False

@InstructionRegistry.register
class IsINF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0], OutputType.PLC)
            ctx.RungStatus = math.isinf(source)

@InstructionRegistry.register
class IsNAN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0], OutputType.PLC)
            ctx.RungStatus = math.isnan(source)