from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class HMIBC(Instruction):
    
    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)
        bit = self.getMemory(self.args[1], OutputType.PLC)

        if not isinstance(value, int) or not isinstance(bit, int):
            raise NotImplementedError("Unsupported HMIBC combination")

        if bit < 0:
            raise ValueError("HMIBC bit index must be >= 0")

        # Clear the specified bit
        result = value & ~(1 << bit)

        self.setMemory(self.args[2], result)