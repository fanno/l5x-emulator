from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

@InstructionRegistry.register
class DTOS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if isinstance(value, int):
                self.setMemory(self.args[1], str(value))
            elif isinstance(value, float):
                self.setMemory(self.args[1], format(value, 'f').rstrip('0').rstrip('.'))
            else:
                raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class STOD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)
            destValue = self.getMemory(self.args[1], OutputType.PLC)

            if not isinstance(value, str):
                raise TypeError("STOD source must be a string")

            if isinstance(destValue, int):
                self.setMemory(self.args[1], int(value))
            elif isinstance(destValue, float):
                self.setMemory(self.args[1], float(value))
            else:
                raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class RTOS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if isinstance(value, float):
                self.setMemory(self.args[1], format(value, 'f').rstrip('0').rstrip('.'))
            else:
                raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class UPPER(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if isinstance(value, str):
                self.setMemory(self.args[1], value.upper())
            else:
                raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class LOWER(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value = self.getMemory(self.args[0], OutputType.PLC)

            if isinstance(value, str):
                self.setMemory(self.args[1], value.lower())
            else:
                raise NotImplementedError(f"{__class__} not implemented yet")