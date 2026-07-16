from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class CPM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class CBIM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class CBSSM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class CSM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class EPMS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class AVC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MMVC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MVC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")