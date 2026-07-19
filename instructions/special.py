from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType
from datatypes.pid import PID as dtPID
from datatypes.custom.datavariant import DataVariant
from datatypes.misc import CONTROL

@InstructionRegistry.register
class FBC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        referance = self.getMemory(self.args[1])
        result = self.getMemory(self.args[2])
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        if ctx.RungStatus:
            if not cmp_control.EN:
                cmp_control.EN.setValue(True)

                if not cmp_control.DN:
                    cmp_control.ER.setValue(False)
                    cmp_control.FD.setValue(False)

                    if cmp_control.LEN <= 0 or cmp_control.POS < 0:
                        cmp_control.ER.setValue(True)
                    else:
                        raise NotImplementedError(f"{__class__} not implemented yet")
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        source = self.getMemory(self.args[0])
        referance = self.getMemory(self.args[1])
        result = self.getMemory(self.args[2])
        cmp_control:CONTROL = self.getMemory(self.args[3])
        result_control:CONTROL = self.getMemory(self.args[4])

        if ctx.RungStatus:
            if not cmp_control.EN:
                cmp_control.EN.setValue(True)

                if not cmp_control.DN:
                    cmp_control.ER.setValue(False)
                    cmp_control.FD.setValue(False)

                    if cmp_control.LEN <= 0 or cmp_control.POS < 0:
                        cmp_control.ER.setValue(True)
                    else:
                        raise NotImplementedError(f"{__class__} not implemented yet")
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

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.getMemory(self.args[0])
            mask = self.getMemory(self.args[1])
            reference = self.getMemory(self.args[2])

            sourceValue = source
            if isinstance(sourceValue, DataVariant):
                sourceValue = sourceValue.getPLCValue()
                
            if isinstance(mask, DataVariant):
                mask = mask.getPLCValue()
            
            referenceValue = reference
            if isinstance(referenceValue, DataVariant):
                referenceValue = referenceValue.getPLCValue()

            maskedSource = sourceValue & mask
            maskedRef = referenceValue & mask

            if maskedSource == maskedRef:
                ctx.RungStatus = False
            else:
                reference.setValue(source)

@InstructionRegistry.register
class PID(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        pv:dtPID = self.getMemory(self.args[0])
        process = self.getMemory(self.args[1])
        tieback = self.getMemory(self.args[2])
        control = self.getMemory(self.args[3])
        PIDMaster = self.getMemory(self.args[4])
        InholdBit = self.getMemory(self.args[5])
        InholdValue = self.getMemory(self.args[6])
        
        if ctx.RungStatus:        
            raise NotImplementedError(f"{__class__} not implemented yet")