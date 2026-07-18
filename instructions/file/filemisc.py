import math
from asyncua.common import Node
from asyncua import ua

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from datatypes.misc import CONTROL

def dint_to_bools(value, count):
    return [(value >> i) & 1 == 1 for i in range(count)]

def bools_to_dint(bools):
    value = 0
    for i, b in enumerate(bools):
        if b:
            value |= (1 << i)
    return value

@InstructionRegistry.register
class FAL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            control:CONTROL = self.getMemory(self.args[0])
            mode = self.args[1]
            '''
            dst = self.getMemory(self.args[2])
            operation = self.getMemory(self.args[3], OutputType.PLC)
            length = self.getMemory(self.args[4], OutputType.PLC)

            if not isinstance(src, list) or not isinstance(dst, list):
                raise NotImplementedError(f"{__class__} not implemented yet")

            if not callable(operation):
                raise NotImplementedError(f"{__class__} not implemented yet")

            for i in range(min(length, len(src))):
                dst[i] = operation(src[i])

            self.setMemory(self.args[1], dst)
            '''

@InstructionRegistry.register
class FSC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            '''
            control:CONTROL = self.getMemory(self.args[0])
            array = self.getMemory(self.args[1], OutputType.PLC)
            target = self.getMemory(self.args[2], OutputType.PLC)
            dest = self.args[3]

            if not isinstance(array, list):
                raise NotImplementedError(f"{__class__} not implemented yet")

            index = -1
            for i, val in enumerate(array):
                if val == target:
                    index = i
                    break

            self.setMemory(dest, index)
            '''

@InstructionRegistry.register
class COP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source:Node = self.getMemory(self.args[0], OutputType.Raw)
            dest:Node = self.getMemory(self.args[1], OutputType.Raw)
            length = self.getMemory(self.args[2], OutputType.PLC)

            if isinstance(source, Node) and isinstance(source, Node):
                sourceDT = await source.read_data_type_as_variant_type()
                destDT = await dest.read_data_type_as_variant_type()

                if sourceDT is not None and destDT is not None:
                    sourceValue = await source.read_value()
                    destValue = await source.read_value()

                    # BOOL[] → DINT
                    if sourceDT == "BOOL_ARRAY" and destDT == "DINT":
                        pass
                        #return bools_to_dint(sourceValue[:32])

                    # DINT → BOOL[]
                    if sourceDT == "DINT" and destDT == "BOOL_ARRAY":
                        pass
                        #return dint_to_bools(sourceValue, length)

                    # Same-type array copy
                    if sourceDT == destDT:
                        pass
                        #return sourceValue[:length].copy()

                    # INT[] → DINT[] (combine pairs)
                    if sourceDT == "INT_ARRAY" and destDT == "DINT_ARRAY":
                        result = []
                        for i in range(0, length * 2, 2):
                            lo = sourceValue[i] & 0xFFFF
                            hi = sourceValue[i+1] & 0xFFFF
                            result.append((hi << 16) | lo)
                        #return result

                    raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class FLL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            sourceValue = self.getMemory(self.args[0], OutputType.PLC)
            destRef:Node = self.getMemory(self.args[1], OutputType.Raw)
            lengthValue = self.getMemory(self.args[2], OutputType.PLC)

            if isinstance(destRef, Node):
                # TODO
                destRefDT:ua.VariantType = await destRef.read_data_type_as_variant_type()

                if destRefDT is not None:
                    destValue = await destRef.read_value()
                    #TODO need to fixe this
                    raise NotImplementedError(f"{__class__} not implemented yet")
                    self.setMemory(self.args[3], sourceValue)

@InstructionRegistry.register
class AVE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            values = self.getMemory(self.args[0], OutputType.PLC)

            if not isinstance(values, list) or not values:
                raise NotImplementedError(f"{__class__} not implemented yet")

            result = sum(values) / len(values)
            self.setMemory(self.args[1], result)

@InstructionRegistry.register
class SRT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        value = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(value, str):
            raise NotImplementedError(f"{__class__} not implemented yet")

        self.setMemory(self.args[1], value)

@InstructionRegistry.register
class STD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        values = self.getMemory(self.args[0], OutputType.PLC)

        if not isinstance(values, list) or not values:
            raise NotImplementedError(f"{__class__} not implemented yet")

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)

        self.setMemory(self.args[1], float(math.sqrt(variance)))

@InstructionRegistry.register
class SIZE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dim = self.args[1]

            sourceRef:Node = self.getMemory(self.args[0], OutputType.Raw)
            
            if isinstance(sourceRef, Node):
                # TODO
                sourceDT:ua.VariantType = await sourceRef.read_data_type_as_variant_type()

                destValue = await sourceRef.read_value()

                self.setMemory(self.args[2], len(destValue))
                #TODO need to fixe this ??? not sure this is working
                #TODO need to also figure out dim to vary
                raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class CPS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        src = self.getMemory(self.args[0], OutputType.PLC)
        dst = self.getMemory(self.args[1], OutputType.PLC)
        length = self.getMemory(self.args[2], OutputType.PLC)

        if not isinstance(src, list) or not isinstance(dst, list):
           raise NotImplementedError(f"{__class__} not implemented yet")

        for i in range(min(length, len(src))):
            dst[i] = src[i]

        self.setMemory(self.args[1], dst)
