from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.misc import CONTROL

from engine.errors import MajorFault

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class SQI(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            array = self.getMemory(self.args[0])
            mask = getPLCValue(self.getMemory(self.args[1]))
            source = getPLCValue(self.getMemory(self.args[2]))
            control:CONTROL = self.getMemory(self.args[3])

            length = getPLCValue(control.LEN)
            position = getPLCValue(control.POS)

            control.ER.setValue(False)

            if length > 0 and position <= 0 and position <= length:
                if position > len(array):
                    control.ER.setValue(True)
                    ctx.RungStatus = False
                else:
                    if (source & mask) != (array[position]):
                        ctx.RungStatus = False
            else:
                control.ER.setValue(True)
                ctx.RungStatus = False
    
@InstructionRegistry.register
class SQO(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[3])

        control.EN.setValue(True)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            array:Array[DataVariant] = self.getMemory(self.args[0])
            mask = getPLCValue(self.getMemory(self.args[1]))
            dest = self.getMemory(self.args[2])
            destValue = getPLCValue(dest)
            control:CONTROL = self.getMemory(self.args[3])

            length = getPLCValue(control.LEN)
            position = getPLCValue(control.POS)

            if length > 0 and position >= 0:
                control.EN.setValue(False)
                if not control.EN:
                    control.EN.setValue(True)
                    control.ER.setValue(False)
                    control.DN.setValue(True)

                    if position < length:
                        position += 1
                    else:
                        position = 1

                    if position == length:
                        control.DN.setValue(True)
                    elif position > length:
                        control.ER.setValue(True)

                    if position > len(array) and False:
                        # TODO: this check is only ControllLogix 5580 implement Controller type check
                        control.ER.setValue(True)
                    else:
                        sequencer_value = getPLCValue(array[position])
                        destValue = (destValue & ~mask) | (sequencer_value & mask)
                        dest.setValue(destValue)
                else:
                    control.DN.setValue(False)
            else:
                control.DN.setValue(False)
                control.EN.setValue(True)
                control.ER.setValue(True)

                if length == position:
                    control.DN.setValue(True)

    
@InstructionRegistry.register
class SQL(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[2])

        control.EN.setValue(True)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        array:Array[DataVariant] = self.getMemory(self.args[1])
        control:CONTROL = self.getMemory(self.args[2])

        length = getPLCValue(control.LEN)
        position = getPLCValue(control.POS)

        if ctx.RungStatus:
            sourceValue = getPLCValue(source)

            if length > 0 and position >= 0:
                if not control.EN:
                    control.EN.setValue(True)
                    control.ER.setValue(False)
                    control.DN.setValue(False)
                    
                    if position < length:
                            position += 1
                    else:
                        position = 1
                else:
                    control.DN.setValue(False)

                if position == length:
                    control.DN.setValue(True)
                else:
                    if position > length:
                        control.ER.setValue(True)

                if not control.ER:
                    if position > len(array):
                        raise MajorFault(4,20)
                    else:
                        array[position].setValue(sourceValue)
            else:
                control.DN.setValue(False)
                control.EN.setValue(True)
                control.ER.setValue(True)

            control.POS.setValue(position)
        else:
            control.EN.setValue(False)
            control.DN.setValue(False)
            control.ER.setValue(False)
        
            if position == length:
                control.DN.setValue(True)
