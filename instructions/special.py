from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MinorFault

from core.registry.instructionregistry import InstructionRegistry
from datatypes.pid import PID as dtPID
from datatypes.misc import CONTROL
from datatypes.custom.array import Array
from datatypes.custom.datavariant import DataVariant

from  instructions.helper import getPLCValue

@InstructionRegistry.register
class FBC(Instruction):

    async def ladder_preScan(self, ctx):
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        cmp_control.EN._reset()
        cmp_control.FD._reset()

        if cmp_control.DN:
            cmp_control.DN._reset()
            cmp_control.POS._reset()
            result_control.DN._reset()
            result_control.POS._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        source:Array[DataVariant] = self.getMemory(self.args[0])
        referance:Array[DataVariant] = self.getMemory(self.args[1])
        result:Array[DataVariant] = self.getMemory(self.args[2])
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        if ctx.RLL.RungStatus: 
            if result_control.POS > len(result):
                raise MinorFault(4, 20)

            if not cmp_control.EN:
                cmp_control.EN.setValue(True)

                if not cmp_control.DN:
                    cmp_control.ER.setValue(False)
                    cmp_control.FD.setValue(False)

                    if cmp_control.LEN <= 0 or cmp_control.POS < 0:
                        cmp_control.ER.setValue(True)
                    else:
                        self.raiseNotImplementedError(ctx)
        else:
            cmp_control.EN.setValue(False)
            cmp_control.FD.setValue(False)
            if cmp_control.DN:
                cmp_control.DN.setValue(False)
                cmp_control.POS.setValue(0)
                result_control.DN.setValue(False)
                result_control.POS.setValue(0)
    
@InstructionRegistry.register
class DDT(Instruction):

    async def ladder_preScan(self, ctx):
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        cmp_control.EN._reset()
        cmp_control.FD._reset()

        if cmp_control.DN:
            cmp_control.DN._reset()
            cmp_control.POS._reset()
            result_control.DN._reset()
            result_control.POS._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        source:Array[DataVariant] = self.getMemory(self.args[0])
        referance:Array[DataVariant] = self.getMemory(self.args[1])
        result:Array[DataVariant] = self.getMemory(self.args[2])
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        if ctx.RLL.RungStatus:
            if result_control.POS > len(result):
                raise MinorFault(4, 20)
                        
            if not cmp_control.EN:
                cmp_control.EN.setValue(True)

                if not cmp_control.DN:
                    cmp_control.ER.setValue(False)
                    cmp_control.FD.setValue(False)

                    if cmp_control.LEN <= 0 or cmp_control.POS < 0:
                        cmp_control.ER.setValue(True)
                    else:
                        self.raiseNotImplementedError(ctx)
        else:
            cmp_control.EN.setValue(False)
            cmp_control.FD.setValue(False)
            if cmp_control.DN:
                cmp_control.DN.setValue(False)
                cmp_control.POS.setValue(0)
                result_control.DN.setValue(False)
                result_control.POS.setValue(0)

@InstructionRegistry.register
class DTR(Instruction):

    async def ladder_preScan(self, ctx):
        source = getPLCValue(self.getMemory(self.args[0]))
        mask = getPLCValue(self.getMemory(self.args[1]))
        reference = self.getMemory(self.args[2])

        maskedSource = source & mask

        reference.setValue(maskedSource)

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = getPLCValue(self.getMemory(self.args[0]))
            mask = getPLCValue(self.getMemory(self.args[1]))
            reference = self.getMemory(self.args[2])
            referenceValue = getPLCValue(reference)

            maskedSource = source & mask
            maskedRef = referenceValue & mask

            if maskedSource == maskedRef:
                ctx.RLL.RungStatus = False
            else:
                reference.setValue(maskedSource)

@InstructionRegistry.register
class PID(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pv:dtPID = self.getMemory(self.args[0])
        process = self.getMemory(self.args[1])
        tieback = self.getMemory(self.args[2])
        control = self.getMemory(self.args[3])
        PIDMaster:dtPID = self.getMemory(self.args[4])
        InholdBit = self.getMemory(self.args[5])
        InholdValue = self.getMemory(self.args[6])
        
        if ctx.RLL.RungStatus:        
            self.raiseNotImplementedError(ctx)