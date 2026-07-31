from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MAW(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MDW(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MAR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MDR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MAOC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MDOC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)