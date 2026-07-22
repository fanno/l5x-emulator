from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MSO(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MSF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MASD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MASR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MDF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MDS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MAFR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")