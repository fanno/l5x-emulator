from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class CPM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class CBIM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class CBSSM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class CSM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class EPMS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class AVC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MMVC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MVC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)