from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.misc import CONTROL

from engine.errors import MajorFault

@InstructionRegistry.register
class SQI(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            array = self.getMemory(self.args[0])
            mask = self.getMemory(self.args[1])
            source = self.getMemory(self.args[2])
            control:CONTROL = self.getMemory(self.args[3])

            if isinstance(mask, DataVariant):
                mask = mask.getPLCValue()
            if isinstance(source):
                source = source.getPLCValue()

            length = control.LEN.getPLCValue()
            position = control.POS.getPLCValue()

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

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            array:Array[DataVariant] = self.getMemory(self.args[0])
            mask = self.getMemory(self.args[1])
            dest = self.getMemory(self.args[2])
            control:CONTROL = self.getMemory(self.args[3])

            if isinstance(mask, DataVariant):
                mask = mask.getPLCValue()
            destValue = dest
            if isinstance(destValue):
                destValue = destValue.getPLCValue()

            length = control.LEN.getPLCValue()
            position = control.POS.getPLCValue()

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
                        sequencer_value = array[position].getPLCValue()
                        destValue = (destValue & ~mask) | (sequencer_value & mask)
                        dest.setPLCValue(destValue)
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        array:Array[DataVariant] = self.getMemory(self.args[1])
        control:CONTROL = self.getMemory(self.args[2])

        length = control.LEN.getPLCValue()
        position = control.POS.getPLCValue()
        if ctx.RungStatus:
            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()

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
                        array[position].setPLCValue(sourceValue)
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
