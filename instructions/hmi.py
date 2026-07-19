from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from  datatypes.misc import HMIBC

@InstructionRegistry.register
class HMIBC(Instruction):
    
    async def execute(self, ctx:"ExecutionContext") -> None:
        value:HMIBC = self.getMemory(self.args[0])
        if ctx.RungStatus:
            # TODO posibly not relevant for pic sim
            raise NotImplementedError(f"{__class__} not implemented yet")