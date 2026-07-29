import math
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from engine.st.helper import hook_expression

from instructions.helper import getPLCValue
from engine.fbd.block import FBDBlock
from typing import Any
from datatypes.fdb import FBD_COMPARE

@InstructionRegistry.register
class CMP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            expression = "return " + hook_expression(self.args[0])

            from engine.st.hooks import run_exec_env
            ctx.RungStatus = await run_exec_env(expression, ctx, "CMP")

@InstructionRegistry.register
class LIM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            aValue = self.getMemory(self.args[0])
            Value = self.getMemory(self.args[1])
            bValue = self.getMemory(self.args[2])
            
            if aValue < bValue:
                if aValue <= Value or bValue >= Value:
                    ctx.RungStatus = False
            else:
                if aValue >= Value or bValue <= Value:
                    ctx.RungStatus = False

@InstructionRegistry.register
class LIMIT(LIM):
    pass

@InstructionRegistry.register
class MEQ(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0])
            maskValue = self.getMemory(self.args[1])
            compageValue = self.getMemory(self.args[2])

            ctx.RungStatus = (sourceValue & maskValue) == (compageValue & maskValue)

@InstructionRegistry.register
class EQU(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA == SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class EQU__F(EQU):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class EQ(EQU):
    pass

@InstructionRegistry.register
class EQ__F(EQU__F):
    pass

@InstructionRegistry.register
class NEQ(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA != SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class NEQ__F(NEQ):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA =  block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)
                
@InstructionRegistry.register
class NE(NEQ):
    pass

@InstructionRegistry.register
class NE__F(NEQ__F):
    pass

@InstructionRegistry.register
class LES(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA < SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class LES__F(LES):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class LT(LES):
    pass

@InstructionRegistry.register
class LT__F(LES__F):
    pass

@InstructionRegistry.register
class GRT(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA > SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value

        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(compare.SourceA, compare.SourceB)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class GRT__F(GRT):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class GT(GRT):
    pass

@InstructionRegistry.register
class GT__F(GRT__F):
    pass


@InstructionRegistry.register
class LEQ(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA <= SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class LEQ__F(LEQ):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class LE(LEQ):
    pass

@InstructionRegistry.register
class LE__F(LEQ__F):
    pass

@InstructionRegistry.register
class GEQ(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return SourceA >= SourceB

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_COMPARE = block.Value
        result = self.execute(compare.SourceA, compare.SourceB)
        compare.Dest.setValue(result)

@InstructionRegistry.register
class GEQ__F(GEQ):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class GE(GEQ):
    pass

@InstructionRegistry.register
class GE__F(GEQ__F):
    pass

@InstructionRegistry.register
class IsINF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            ctx.RungStatus = math.isinf(source)

@InstructionRegistry.register
class IsNAN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            ctx.RungStatus = math.isnan(source)