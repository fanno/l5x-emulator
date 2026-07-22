from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MajorFault

from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType

from datatypes.misc import CONTROL
from datatypes.custom.array import Array
from datatypes.custom.numbers import DINT

from datatypes.custom.datavariant import DataVariant

from datatypes.custom.udt import Resettable

@InstructionRegistry.register
class BSL(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[1])

        control.EN._reset()
        control.DN._reset()
        control.ER._reset()
        control.POS._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value:Array[DataVariant] = self.getMemory(self.args[0])
            control:CONTROL = self.getMemory(self.args[1])
            source = self.getMemory(self.args[2])
            
            len = control.LEN

            #TODO: SHIFT ARRAY
            listValue = value.getPLCValue()

@InstructionRegistry.register
class BSR(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[1])

        control.EN._reset()
        control.DN._reset()
        control.ER._reset()
        control.POS._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            value:Array[DataVariant] = self.getMemory(self.args[0])
            control:CONTROL = self.getMemory(self.args[1])
            source = self.getMemory(self.args[2])

            len = control.LEN

            #TODO: SHIFT ARRAY
            listValue = value.getPLCValue()

@InstructionRegistry.register
class FFL(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[2])

        control.EN.setValue(True)

        if control.LEN <= 0 or control.POS < 0:
            control.EM.setValue(True)
            control.DN.setValue(True)
        else:
            control.EM.setValue(False)
            control.DN.setValue(False)

            if control.POS == 0:
                control.EM.setValue(True)
            if control.POS >= control.LEN:
                control.DN.setValue(True)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        control:CONTROL = self.getMemory(self.args[2])
        if ctx.RungStatus:
            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if not control.EN:
                    control.EN.setValue(True)

                    control.POS += 1
                    
                    if control.POS >= control.LEN:
                        control.DN.setValue(True)

                    if control.POS > control.LEN:
                        control.POS -= 1
                    else:
                        source:DataVariant = self.getMemory(self.args[0])
                        fifo:Array[DataVariant] = self.getMemory(self.args[1])

                        if len(fifo) >= control.POS:
                            raise MajorFault(4, 20)
                        else:
                            fifo[control.POS] = source
        else:
            control.EN.setValue(False)

            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if control.POS == 0:
                    control.EM.setValue(True)

                if control.POS >= control.LEN:
                    control.DN.setValue(True)

@InstructionRegistry.register
class FFU(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[2])

        control.EU.setValue(True)

        if control.LEN <= 0 or control.POS < 0:
            control.EM.setValue(True)
            control.DN.setValue(True)
        else:
            control.EM.setValue(False)
            control.DN.setValue(False)

            if control.POS == 0:
                control.EM.setValue(True)
            if control.POS >= control.LEN:
                control.DN.setValue(True)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        control:CONTROL = self.getMemory(self.args[2])
        if ctx.RungStatus:
            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if not control.EU:
                    control.EU.setValue(True)

                    fifo:Array[DataVariant] = self.getMemory(self.args[0])
                    dest:DataVariant = self.getMemory(self.args[1])

                    if control.POS <= 1:
                        control.EM.setValue(True)

                    if control.POS < 1:
                        if isinstance(dest, Resettable):
                            dest._reset()
                    else:
                        if control.POS > control.LEN:
                            control.POS.setValue(control.LEN.getPLCValue())

                        control.POS -= 1

                        if len(fifo) < control.LEN:
                            raise MajorFault(4, 20)
                        else:
                            dest.setValue(fifo[0].copy())

                            for i in range(control.POS.getPLCValue(), control.LEN + 1):
                                fifo[i] = fifo[i+1]
                            if isinstance(fifo[control.LEN - 1], Resettable):
                                fifo[control.LEN - 1]._reset()
                else:
                    if control.POS == 0:
                        control.EM.setValue(True)
                    
                    if control.POS >= control.POS :
                        control.DN.setValue(True)
        else:
            control.EU.setValue(False)

            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if control.POS == 0:
                    control.EM.setValue(True)

                if control.POS >= control.LEN:
                    control.DN.setValue(True)
    
@InstructionRegistry.register
class LFL(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[2])

        control.EN.setValue(True)

        if control.LEN <= 0 or control.POS < 0:
            control.EM.setValue(True)
            control.DN.setValue(True)
        else:
            control.EM.setValue(False)
            control.DN.setValue(False)

            if control.POS == 0:
                control.EM.setValue(True)
            if control.POS >= control.LEN:
                control.DN.setValue(True)    

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        control:CONTROL = self.getMemory(self.args[2])
        if ctx.RungStatus:
            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if not control.EN:
                    control.EN.setValue(True)

                    control.POS += 1
                    
                    if control.POS >= control.LEN:
                        control.DN.setValue(True)

                    if control.POS > control.LEN:
                        control.POS -= 1
                    else:
                        source:DataVariant = self.getMemory(self.args[0])
                        fifo:Array[DataVariant] = self.getMemory(self.args[1])

                        if len(fifo) >= control.POS:
                            raise MajorFault(4, 20)
                        else:
                            fifo[control.POS] = source
        else:
            control.EN.setValue(False)

            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if control.POS == 0:
                    control.EM.setValue(True)

                if control.POS >= control.LEN:
                    control.DN.setValue(True)
    
@InstructionRegistry.register
class LFU(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        control:CONTROL = self.getMemory(self.args[2])

        control.EU.setValue(True)

        if control.LEN <= 0 or control.POS < 0:
            control.EM.setValue(True)
            control.DN.setValue(True)
        else:
            control.EM.setValue(False)
            control.DN.setValue(False)

            if control.POS == 0:
                control.EM.setValue(True)
            if control.POS >= control.LEN:
                control.DN.setValue(True)        

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        control:CONTROL = self.getMemory(self.args[2])
        if ctx.RungStatus:
            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if not control.EU:
                    control.EU.setValue(True)

                    fifo:Array[DataVariant] = self.getMemory(self.args[0])
                    dest:DataVariant = self.getMemory(self.args[1])

                    if control.POS <= 1:
                        control.EM.setValue(True)

                    if control.POS < 1:
                        if isinstance(dest, Resettable):
                            dest._reset()
                    else:
                        if control.POS > control.LEN:
                            control.POS.setValue(control.LEN.getPLCValue())

                        if len(fifo) < control.LEN:
                            raise MajorFault(4, 20)
                        else:
                            dest.setValue(fifo[control.POS].copy())

                            if isinstance(fifo[control.POS], Resettable):
                                fifo[control.POS]._reset()

                        control.POS -= 1
                else:
                    if control.POS == 0:
                        control.EM.setValue(True)
                    
                    if control.POS >= control.POS :
                        control.DN.setValue(True)
        else:
            control.EU.setValue(False)

            if control.LEN <= 0 or control.POS < 0:
                control.DN.setValue(True)
                control.EM.setValue(True)
            else:
                control.DN.setValue(False)
                control.EM.setValue(False)

                if control.POS == 0:
                    control.EM.setValue(True)

                if control.POS >= control.LEN:
                    control.DN.setValue(True)