from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MGS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MGSD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MGSR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MGSP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)