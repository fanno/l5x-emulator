import math

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class LN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            if not isinstance(source, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")
            if source <= 0:
                raise NotImplementedError(f"{__class__} not implemented yet")

            dest.setValue(float(math.log(source)))

@InstructionRegistry.register
class LOG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            if not isinstance(source, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")
            if source <= 0:
                raise NotImplementedError(f"{__class__} not implemented yet")
            
            dest.setValue(float(math.log10(source)))

@InstructionRegistry.register
class XPY(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            x = getPLCValue(self.getMemory(self.args[0]))
            y = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise NotImplementedError(f"{__class__} not implemented yet")

            dest.setValue(float(math.pow(x, y)))

@InstructionRegistry.register
class EXPT(XPY):
    pass