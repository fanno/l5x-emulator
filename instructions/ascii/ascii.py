from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class FIND(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceAValue = self.getMemory(self.args[0], OutputType.PLC)
            sourceBValue = self.getMemory(self.args[1], OutputType.PLC)
            startValue = self.getMemory(self.args[2], OutputType.PLC)
            
            self.setMemory(self.args[3], sourceAValue.find(sourceBValue, startValue))

@InstructionRegistry.register
class INSERT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceAValue = self.getMemory(self.args[0], OutputType.PLC)
            sourceBValue = self.getMemory(self.args[1], OutputType.PLC)
            startValue = self.getMemory(self.args[2], OutputType.PLC)
            
            destValue = sourceAValue[:startValue] + sourceBValue + sourceAValue[startValue:]
            self.setMemory(self.args[3], destValue)

@InstructionRegistry.register
class CONCAT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceAValue = self.getMemory(self.args[0], OutputType.PLC)
            sourceBValue = self.getMemory(self.args[1], OutputType.PLC)

            self.setMemory(self.args[2], sourceAValue + sourceBValue)

@InstructionRegistry.register
class MID(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0], OutputType.PLC)
            qtyValue = self.getMemory(self.args[1], OutputType.PLC)
            startValue = self.getMemory(self.args[2], OutputType.PLC)

            self.setMemory(self.args[3], sourceValue[startValue:startValue+qtyValue])

@InstructionRegistry.register
class DELETE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0], OutputType.PLC)
            qtyValue = self.getMemory(self.args[1], OutputType.PLC)
            startValue = self.getMemory(self.args[2], OutputType.PLC)

            self.setMemory(self.args[3], sourceValue[:startValue] + sourceValue[startValue + qtyValue:])
