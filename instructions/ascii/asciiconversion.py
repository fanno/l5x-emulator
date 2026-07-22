from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.custom.numbers import INTIGER, REAL

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class DTOS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            value = ''
            if isinstance(source, INTIGER):
                value = str(sourceValue)
            elif isinstance(source, REAL):
                value = format(sourceValue, 'f').rstrip('0').rstrip('.')

            dest.setValue(value)

@InstructionRegistry.register
class STOD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            dest.setValue(sourceValue)

@InstructionRegistry.register
class RTOS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            dest.setValue(format(sourceValue, 'f').rstrip('0').rstrip('.'))
            
@InstructionRegistry.register
class STOR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            dest.setValue(sourceValue)


@InstructionRegistry.register
class UPPER(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            dest.setValue(sourceValue.upper())

@InstructionRegistry.register
class LOWER(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            sourceValue = getPLCValue(source)
            dest = self.getMemory(self.args[1])

            dest.setValue(sourceValue.lower())