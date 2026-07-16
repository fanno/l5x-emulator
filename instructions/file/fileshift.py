from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class BSL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, int):
            raise NotImplementedError("Unsupported BSL combination")

        self.setMemory(self.args[1], value << 1)

@InstructionRegistry.register
class BSR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, int):
            raise NotImplementedError("Unsupported BSR combination")

        self.setMemory(self.args[1], value >> 1)

@InstructionRegistry.register
class FFL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0], OutputType.PLC)
        fifo = self.getMemory(self.args[1], OutputType.PLC)
        length = self.getMemory(self.args[2], OutputType.PLC)

        if not isinstance(fifo, list) or not isinstance(length, int):
            raise NotImplementedError("Unsupported FFL combination")

        if len(fifo) < length:
            fifo.append(source)

        self.setMemory(self.args[1], fifo)
        self.setMemory(self.args[3], len(fifo))
    
@InstructionRegistry.register
class LFL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0], OutputType.PLC)
        stack = self.getMemory(self.args[1], OutputType.PLC)
        dest = self.args[2]

        if not isinstance(stack, list):
            raise NotImplementedError("Unsupported LFL combination")

        stack.append(source)

        self.setMemory(self.args[1], stack)
        self.setMemory(dest, len(stack))

    
@InstructionRegistry.register
class LFU(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        stack = self.getMemory(self.args[0], OutputType.PLC)
        
        if not isinstance(stack, list):
            raise NotImplementedError("Unsupported LFU combination")

        if not stack:
            raise ValueError("LFU stack underflow")

        value = stack.pop()

        self.setMemory(self.args[0], stack)
        self.setMemory(self.args[1], value)