from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class XIC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= bool(self.getMemory(self.args[0], OutputType.PLC))

@InstructionRegistry.register
class XIO(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= not bool(self.getMemory(self.args[0], OutputType.PLC))

@InstructionRegistry.register
class OTE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        self.setMemory(self.args[0], ctx.RungStatus)

@InstructionRegistry.register
class OTL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.setMemory(self.args[0], True)

@InstructionRegistry.register
class OTU(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            self.setMemory(self.args[0], False)

@InstructionRegistry.register
class ONS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0], OutputType.PLC)
        self.setMemory(self.args[0], ctx.RungStatus)
        if ons and ctx.RungStatus:
            ctx.RungStatus = False

@InstructionRegistry.register
class OSR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Sbit = self.args[0]
            Obit = self.args[1]

            ons = self.getMemory(Sbit, OutputType.PLC)
            if ons:
                self.setMemory(Obit, False)
            else:
                self.setMemory(Obit, True)
            self.setMemory(Sbit, True)
        
@InstructionRegistry.register
class OSF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        Sbit = self.args[0]
        Obit = self.args[1]

        if ctx.RungStatus:
            self.setMemory(Sbit, True)
            self.setMemory(Obit, False)
        else:
            ons = self.getMemory(Sbit, OutputType.PLC)
            if ons:
                self.setMemory(Obit, True)
            else:
                self.setMemory(Obit, False)
            self.setMemory(Sbit, False)