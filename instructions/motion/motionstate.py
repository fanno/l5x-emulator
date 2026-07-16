from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MSO(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MSF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MASD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MASR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MDF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MDS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MAFR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass