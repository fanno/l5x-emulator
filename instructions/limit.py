from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class ESEL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class SSUM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class SNEG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class HLL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class RLIM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)