from asyncua.common import Node
from asyncua import ua

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType
from instructions.helper import _AND, _OR, _XOR, _NOT

@InstructionRegistry.register
class MOV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            result = self.getMemory(self.args[0], OutputType.PLC)
            self.setMemory(self.args[1], result)
            
@InstructionRegistry.register
class MVM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.args[0]
            mask = self.args[1]
            dest = self.args[2]

            sourceValue = self.getMemory(source, OutputType.PLC)
            maskValue = self.getMemory(mask, OutputType.PLC)

            destValue = self.getMemory(dest, OutputType.PLC)

            bit_width=32 ## TODO:set depending on mask length or source or dest length ?
            
            full_mask = (1 << bit_width) - 1
            maskValue &= full_mask
            destValue = (destValue & ~maskValue) | (sourceValue & maskValue)

            self.setMemory(dest, destValue)

@InstructionRegistry.register
class AND(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = self.args[0]
            sourceB = self.args[1]
            dest = self.args[2]

            sourceAValue = self.getMemory(sourceA, OutputType.PLC)
            sourceBValue = self.getMemory(sourceB, OutputType.PLC)

            destValue = _AND(sourceAValue, sourceBValue, 32) # should be 64 ?

            self.setMemory(dest, destValue)

@InstructionRegistry.register
class OR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = self.args[0]
            sourceB = self.args[1]
            dest = self.args[2]

            sourceAValue = self.getMemory(sourceA, OutputType.PLC)
            sourceBValue = self.getMemory(sourceB, OutputType.PLC)

            destValue = _OR(sourceAValue, sourceBValue, 32) # should be 64 ?

            self.setMemory(dest, destValue)

@InstructionRegistry.register
class XOR(Instruction):
    
    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = self.args[0]
            sourceB = self.args[1]
            dest = self.args[2]

            sourceAValue = self.getMemory(sourceA, OutputType.PLC)
            sourceBValue = self.getMemory(sourceB, OutputType.PLC)

            destValue = _XOR(sourceAValue, sourceBValue, 32) # should be 64 ?

            self.setMemory(dest, destValue)

@InstructionRegistry.register
class NOT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceA = self.args[0]
            dest = self.args[1]

            sourceAValue = self.getMemory(sourceA, OutputType.PLC)

            destValue = _NOT(sourceAValue, 32) # should be 64?
            ## TODO length depend on data size in dest ?

            self.setMemory(dest, destValue)

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
            sourceA = self.args[0]
            orderMode = self.args[1]
            dest = self.args[2]

            sourceAValue = self.getMemory(sourceA, OutputType.PLC)

            width = 32 ## should come from data type

            if width not in (16, 32):
                raise ValueError("SWPB supports only INT (16) or DINT (32)")

            byte_count = width // 8
            bytes_ = _to_bytes(sourceAValue, byte_count)

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

            self.setMemory(dest, destValue)

@InstructionRegistry.register
class CLR(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dest = self.args[0]

            destRef:Node = self.getMemory(dest, OutputType.Raw)


            if isinstance(destRef, Node):
                destRefDT:ua.VariantType = await destRef.read_data_type_as_variant_type()

                if destRefDT is not None:
                    match destRefDT:
                        case ua.VariantType.Double | ua.VariantType.Float | ua.VariantType.Int16 | ua.VariantType.Int32 | ua.VariantType.Int64 | ua.VariantType.UInt16 | ua.VariantType.UInt32 | ua.VariantType.UInt64 | ua.VariantType:
                            self.setMemory(dest, 0)
                        case _:
                            #TODO TIME and other objects
                            raise ValueError("Invalid CLR type")

@InstructionRegistry.register
class BTD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.args[0]
            sourceBit = self.args[1]
            dest = self.args[2]
            destBit = self.args[3]
            length = self.args[4]

            sourceRef:Node = self.getMemory(source, OutputType.Raw)
            sourceBitValue = self.getMemory(sourceBit, OutputType.PLC)
            destRef:Node = self.getMemory(dest, OutputType.Raw)
            destBitValue = self.getMemory(destBit, OutputType.PLC)
            lengthValue = self.getMemory(length, OutputType.PLC)

            if isinstance(sourceRef, Node) and isinstance(destRef, Node):
                sourceRefDT:ua.VariantType = await sourceRef.read_data_type_as_variant_type()
                destRefDT:ua.VariantType = await destRef.read_data_type_as_variant_type()

                if sourceRefDT is not None and destRefDT is not None:
                    destValue = await destRef.read_value()
                    
                    width:int = 32 #TODO from datatype

                    if not (0 <= sourceBitValue < width):
                        raise ValueError("source_bit out of range")
                    if not (0 <= destBitValue < width):
                        raise ValueError("dest_bit out of range")
                    if lengthValue <= 0:
                        return destValue
                    if sourceBitValue + length > width:
                        raise ValueError("source range exceeds width")
                    if destBitValue + length > width:
                        raise ValueError("dest range exceeds width")

                    mask = ((1 << length) - 1) << destBitValue

                    bits = ((source >> sourceBitValue) & ((1 << length) - 1)) << destBitValue

                    destValue = (destValue & ~mask) | bits

                    self.setMemory(dest, destValue)

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