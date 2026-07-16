from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType
from datatypes.pid import PID as dtPID

@InstructionRegistry.register
class FBC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            a_value = self.getMemory(self.args[0], OutputType.PLC)
            b_value = self.getMemory(self.args[1], OutputType.PLC)

            result = 1 if (a_value == b_value) else 0

            self.setMemory(self.args[2], result)
            #TODO
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DDT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], value)
            #TODO
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class DTR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            self.setMemory(self.args[1], float(value))
            #TODO
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class PID(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            pv:dtPID = self.getMemory(self.args[0])
            process = self.getMemory(self.args[1])
            tieback = self.getMemory(self.args[2])
            control = self.getMemory(self.args[3])
            PIDMaster = self.getMemory(self.args[4])
            InholdBit = self.getMemory(self.args[5])
            InholdValue = self.getMemory(self.args[6])

            #TODO
            raise NotImplementedError(f"{__class__} not implemented yet")