from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class SFX(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SS1(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SS2(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SBC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SOS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SDI(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SLS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SLP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")