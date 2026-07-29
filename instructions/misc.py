from engine.context import ExecutionContext

from engine.instruction import Instruction

from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class BRT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pass
        ##  DO NOTHING in simulation

@InstructionRegistry.register
class TPT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pass
        ##  DO NOTHING in simulation
