from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.custom.numbers import INTIGER, REAL

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class DTOS(Instruction):

    def execute(self, Source) -> str:
        sourceValue = getPLCValue(Source)

        value = ''
        if isinstance(Source, INTIGER):
            value = str(sourceValue)
        elif isinstance(Source, REAL):
            value = format(sourceValue, 'f').rstrip('0').rstrip('.')        
        
        return value
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))      

@InstructionRegistry.register
class STOD(Instruction):
    def execute(self, Source) -> int:
        Source = self.getMemory(self.args[0])
        return getPLCValue(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))  

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))                 

@InstructionRegistry.register
class RTOS(Instruction):

    def execute(self, Source) -> str:
        sourceValue = getPLCValue(Source)
        return format(sourceValue, 'f').rstrip('0').rstrip('.')
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))
            
@InstructionRegistry.register
class STOR(Instruction):

    def execute(self, Source) -> float:
        Source = self.getMemory(self.args[0])
        return getPLCValue(Source)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))          

@InstructionRegistry.register
class UPPER(Instruction):

    def execute(self, Source) -> str:
        sourceValue = getPLCValue(Source)
        return sourceValue.upper()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))

@InstructionRegistry.register
class LOWER(Instruction):

    def execute(self, Source) -> str:
        sourceValue = getPLCValue(Source)
        return sourceValue.lower()    

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.getMemory(self.args[0])
            dest = self.getMemory(self.args[1])
            dest.setValue(self.execute(source))

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        dest = self.getMemory(self.args[1])
        dest.setValue(self.execute(source))