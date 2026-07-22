from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class FOR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        rutine = self.args[0]
        index = self.getMemory(self.args[1])

        start = getPLCValue(self.getMemory(self.args[2]))
        end = getPLCValue(self.getMemory(self.args[3]))
        step = getPLCValue(self.getMemory(self.args[4]))

        for i in range(start, end+1, step):
            index.setValue(i)

            context = ExecutionContext(ProgramRef=ctx.ProgramRef)
            await ctx.ProgramRef.Routines[rutine].execute(context)
    
@InstructionRegistry.register
class BRK(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.TND = True