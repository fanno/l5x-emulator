from asyncua.common import Node
from asyncua import ua

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType
from instructions.helper import _AND, _OR, _XOR, _NOT

from datatypes.custom.udt import Resettable

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class MOV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            result = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            dest.setValue(result)

@InstructionRegistry.register
class MOVE(MOV):
    pass
            
@InstructionRegistry.register
class MVM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = getPLCValue(self.getMemory(self.args[0]))
            sourceB = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            destValue = _AND(sourceA, sourceB, 32) # should be 64 ?

            dest.setValue(destValue)

@InstructionRegistry.register
class OR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = getPLCValue(self.getMemory(self.args[0]))
            sourceB = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            destValue = _OR(sourceA, sourceB, 32) # should be 64 ?

            dest.setValue(destValue)

@InstructionRegistry.register
class XOR(Instruction):
    
    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = getPLCValue(self.getMemory(self.args[0]))
            sourceB = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])

            destValue = _XOR(sourceA, sourceB, 32) # should be 64 ?

            dest.setValue(destValue)

@InstructionRegistry.register
class NOT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = getPLCValue(self.getMemory(self.args[0]))
            dest = self.getMemory(self.args[1])

            destValue = _NOT(sourceA, 64) # should be 64?
            ## TODO length depend on data size in dest ?

            dest.setValue(destValue)

def _to_bytes(value: int, byte_count: int) -> list[int]:
    return [(value >> (8 * i)) & 0xFF for i in range(byte_count)]

def _from_bytes(bytes_):
    value = 0
    for i, b in enumerate(bytes_):
        value |= (b & 0xFF) << (8 * i)
    return value

@InstructionRegistry.register
class SWPB(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dest = self.getMemory(self.args[0])
            if isinstance(dest, Resettable):
                dest._reset()

@InstructionRegistry.register
class BTD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class BTDT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class DFF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class JKFF(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SETD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class RESD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")