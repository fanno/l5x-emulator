from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from datatypes.custom.numbers import INTIGER, REAL
from datatypes.custom.string import STRING
from datatypes.custom.datavariant import DataVariant

@InstructionRegistry.register
class DTOS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            value = ''
            if isinstance(source, INTIGER):
                value = str(sourceValue)
            elif isinstance(source, REAL):
                value = format(sourceValue, 'f').rstrip('0').rstrip('.')

            dest.setValue(value)

@InstructionRegistry.register
class STOD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            dest.setValue(sourceValue)

@InstructionRegistry.register
class RTOS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            dest.setValue(format(sourceValue, 'f').rstrip('0').rstrip('.'))
            
@InstructionRegistry.register
class STOR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            dest.setValue(sourceValue)


@InstructionRegistry.register
class UPPER(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            dest.setValue(sourceValue.upper())

@InstructionRegistry.register
class LOWER(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

            dest.setValue(sourceValue.lower())