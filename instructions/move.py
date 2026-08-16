from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from instructions.helper import _AND, _OR, _XOR, _NOT

from  instructions.helper import getPLCValue
from datatypes.fdb import FBD_LOGICAL, FBD_BOOLEAN_AND, FBD_BOOLEAN_NOT, FBD_BOOLEAN_XOR, FBD_BOOLEAN_OR
from typing import Any
from engine.fbd.block import FBDBlock

from protocols.memory import Resettable

from utils.isplcinstance import isPLCInstance

@InstructionRegistry.register
class MOV(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            result = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(result)

@InstructionRegistry.register
class MOVE(MOV):
    pass
            
@InstructionRegistry.register
class MVM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            mask = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])
            destValue = getPLCValue(dest)

            bit_width=64 ## TODO:set depending on mask length or source or dest length ?
            
            full_mask = (1 << bit_width) - 1
            mask &= full_mask
            destValue = (destValue & ~mask) | (source & mask)

            dest.setValue(destValue)

@InstructionRegistry.register
class AND(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return _AND(SourceA, SourceB, 64)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RLL.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_LOGICAL = block.Value
        if compare.EnableIn:
            compare.Dest.setValue(self.execute(compare.SourceA, compare.SourceB))
        compare.EnableOut.setValue(compare.EnableIn)

class AND__F(AND):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class OR(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return _OR(SourceA, SourceB, 64)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RLL.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_LOGICAL = block.Value
        if compare.EnableIn:
            compare.Dest.setValue(self.execute(compare.SourceA, compare.SourceB))
        compare.EnableOut.setValue(compare.EnableIn)

class OR__F(OR):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class XOR(Instruction):

    def execute(self, SourceA, SourceB) -> Any:
        SourceA = getPLCValue(SourceA)
        SourceB = getPLCValue(SourceB)
        return _XOR(SourceA, SourceB, 64)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            SourceA = self.getMemory(self.args[0])
            SourceB = self.getMemory(self.args[1])
            
            result = self.execute(SourceA, SourceB)
            if not result:
                ctx.RLL.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_LOGICAL = block.Value
        if compare.EnableIn:
            compare.Dest.setValue(self.execute(compare.SourceA, compare.SourceB))
        compare.EnableOut.setValue(compare.EnableIn)

class XOR__F(XOR):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        SourceA = block.inParams["SourceA"].Value
        SourceB = block.inParams["SourceB"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(SourceA, SourceB)

@InstructionRegistry.register
class NOT(Instruction):

    def execute(self, Source) -> Any:
        Source = getPLCValue(Source)
        return _NOT(Source, 64)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Source = self.getMemory(self.args[0])
            
            result = self.execute(Source)
            if not result:
                ctx.RLL.RungStatus = False

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_LOGICAL = block.Value
        if compare.EnableIn:
            compare.Dest.setValue(self.execute(compare.Source))
        compare.EnableOut.setValue(compare.EnableIn)

class NOT__F(NOT):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        Source = block.inParams["Source"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = self.execute(Source)        

def _to_bytes(value: int, byte_count: int) -> list[int]:
    return [(value >> (8 * i)) & 0xFF for i in range(byte_count)]

def _from_bytes(bytes_):
    value = 0
    for i, b in enumerate(bytes_):
        value |= (b & 0xFF) << (8 * i)
    return value

@InstructionRegistry.register
class SWPB(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            sourceA = getPLCValue(self.getMemory(self.args[0]))
            orderMode = self.args[1]
            dest = self.getMemory(self.args[2])

            width = 32 ## should come from data type

            if width not in (16, 32):
                raise ValueError("SWPB supports only INT (16) or DINT (32)")

            byte_count = width // 8
            bytes_ = _to_bytes(sourceA, byte_count)

            match orderMode:
                case "REVERSE":
                    bytes_.reverse()
                case "WORD":
                    if width != 32:
                        raise ValueError("word mode valid only for DINT")
                    bytes_ = bytes_[2:4] + bytes_[0:2]
                case "HIGH/LOW":
                    for i in range(0, byte_count, 2):
                        bytes_[i], bytes_[i + 1] = bytes_[i + 1], bytes_[i]
                case _:
                    raise ValueError("Invalid SWPB order mode")

            destValue = _from_bytes(bytes_)

            dest.setValue(destValue)

@InstructionRegistry.register
class CLR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            dest = self.getMemory(self.args[0])
            if isPLCInstance(dest, Resettable):
                dest._reset()

@InstructionRegistry.register
class BTD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            sourceBit = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])
            destVal = getPLCValue(dest)
            destBit = getPLCValue(self.getMemory(self.args[3]))
            length = getPLCValue(self.getMemory(self.args[4]))

            for i in range(length):
                dest_clear_mask = ~(1 << (destBit + i))
                destVal = destVal & dest_clear_mask
                
                src_bit_val = (source >> (sourceBit + i)) & 1
                
                if src_bit_val:
                    destVal = destVal | (1 << (destBit + i))

            dest.setValue(destVal)

@InstructionRegistry.register
class MVMT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class BTDT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class DFF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class JKFF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class SETD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class RESD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class BOR(Instruction):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_BOOLEAN_OR = block.Value

        if compare.EnableIn:
            result = compare.In1 or compare.In2 or compare.In3 or compare.In4 or compare.In5 or compare.In6 or compare.In7 or compare.In8
            compare.Out.setValue(result)
        compare.EnableOut.setValue(compare.EnableIn)

class BOR__F(BOR):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        In1 = block.inParams["In1"].Value
        In2 = block.inParams["In2"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = In1 or In2  

@InstructionRegistry.register
class BNOT(Instruction):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_BOOLEAN_NOT = block.Value

        if compare.EnableIn:
            result = not compare.In
            compare.Out.setValue(result)
        compare.EnableOut.setValue(compare.EnableIn)

class BNOT__F(BNOT):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        In = block.inParams["In"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = not In

@InstructionRegistry.register
class BXOR(Instruction):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_BOOLEAN_XOR = block.Value

        if compare.EnableIn:
            result = compare.In1 != compare.In2

            compare.Out.setValue(result)
        compare.EnableOut.setValue(compare.EnableIn)

class BXOR__F(BXOR):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        In1 = block.inParams["In1"].Value
        In2 = block.inParams["In2"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = In1 != In2

@InstructionRegistry.register
class BAND(Instruction):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        compare:FBD_BOOLEAN_AND = block.Value

        if compare.EnableIn:
            result = compare.In1 and compare.In2 and compare.In3 and compare.In4 and compare.In5 and compare.In6 and compare.In7 and compare.In8

            compare.Out.setValue(result)
        compare.EnableOut.setValue(compare.EnableIn)

class BAND__F(BAND):

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        In1 = block.inParams["In1"].Value
        In2 = block.inParams["In2"].Value
        Dest = block.outParams["Dest"]

        Dest.Value = In1 and In2