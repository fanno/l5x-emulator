from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from datatypes.custom.datavariant import DataVariant

@InstructionRegistry.register
class XIC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= bool(self.getMemory(self.args[0]))

@InstructionRegistry.register
class XIO(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= not bool(self.getMemory(self.args[0]))

@InstructionRegistry.register
class OTE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        self.setMemory(self.args[0], ctx.RungStatus)

@InstructionRegistry.register
class OTL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.setMemory(self.args[0], True)

@InstructionRegistry.register
class OTU(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.setMemory(self.args[0], False)

@InstructionRegistry.register
class ONS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])

        ons.setValue(ctx.RungStatus)
        if ons and ctx.RungStatus:
            ctx.RungStatus = False

@InstructionRegistry.register
class OSR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])
        out = self.getMemory(self.args[1])

        out.setValue(False)
        if ctx.RungStatus:
            if not ons:
                out.setValue(True)
        ons.setValue(ctx.RungStatus)
        
@InstructionRegistry.register
class OSF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])
        out = self.getMemory(self.args[1])

        out.setValue(False)
        if not ctx.RungStatus:
            if ons:
                out.setValue(True)
        ons.setValue(ctx.RungStatus)