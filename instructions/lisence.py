from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class LV(Instruction):
    
    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError("Unsupported LV combination")