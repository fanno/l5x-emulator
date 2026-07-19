from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.custom.datavariant import DataVariant

@InstructionRegistry.register
class FOR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        rutine = self.args[0]
        index = self.getMemory(self.args[1])
        start = self.getMemory(self.args[2])
        end = self.getMemory(self.args[3])
        step = self.getMemory(self.args[4])

        if isinstance(start, DataVariant):
            start = start.getPLCValue()
        if isinstance(end, DataVariant):
            end = end.getPLCValue()
        if isinstance(step, DataVariant):
            step = step.getPLCValue()

        for i in range(start, end+1, step):
            index.setValue(i)

            context = ExecutionContext(ProgramRef=ctx.ProgramRef)
            await ctx.ProgramRef.Routines[self.args[0]].execute(context)
    
@InstructionRegistry.register
class BRK(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.TND = True