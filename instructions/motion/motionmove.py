from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MAS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MAH(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MAJ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MAM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MAG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MCD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MRP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MCCP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MCSV(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MAPC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MATC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class MDAC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)