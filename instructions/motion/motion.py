from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MAW(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MDW(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MAR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MDR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MAOC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MDOC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")