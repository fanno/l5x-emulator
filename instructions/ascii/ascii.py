from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class FIND(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA:str = getPLCValue(self.getMemory(self.args[0]))
            sourceB:str = getPLCValue(self.getMemory(self.args[1]))
            start:int = getPLCValue(self.getMemory(self.args[2]))
            find = self.getMemory(self.args[3])

            find.setValue(sourceA.find(sourceB, start))

@InstructionRegistry.register
class INSERT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA:str = getPLCValue(self.getMemory(self.args[0]))
            sourceB:str = getPLCValue(self.getMemory(self.args[1]))
            start:int = getPLCValue(self.getMemory(self.args[2]))
            dest = self.getMemory(self.args[3])            

            destValue = sourceA[:start] + sourceB + sourceA[start:]
            dest.setValue(destValue)

@InstructionRegistry.register
class CONCAT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA:str = getPLCValue(self.getMemory(self.args[0]))
            sourceB:str = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            dest.setValue(sourceA + sourceB)

@InstructionRegistry.register
class MID(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source:str = getPLCValue(self.getMemory(self.args[0]))
            qty:int = getPLCValue(self.getMemory(self.args[1]))
            start:int = getPLCValue(self.getMemory(self.args[2]))
            dest = self.getMemory(self.args[3])

            dest.setValue(source[start:start+qty])

@InstructionRegistry.register
class DELETE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source:str = getPLCValue(self.getMemory(self.args[0]))
            qty:int = getPLCValue(self.getMemory(self.args[1]))
            start:int = getPLCValue(self.getMemory(self.args[2]))
            dest = self.getMemory(self.args[3])

            dest.setValue(source[:start] + source[start + qty:])