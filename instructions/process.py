from engine.context import ExecutionContext

from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from datatypes.alarm import ALARM
from datatypes.pid import PID_ENHANCED


@InstructionRegistry.register
class ALM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        timer:ALARM = self.getMemory(self.args[0])

        self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class SCL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        tag = self.args[0]

        self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class PIDE(Instruction):

    async def ladder_preScan(self, ctx):
        pide:PID_ENHANCED = self.getMemory(self.args[0])
        
        pide.EnableIn._reset()
        pide.EnableOut._reset()


    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pide:PID_ENHANCED = self.getMemory(self.args[0])

        if pide.EnableIn:
            self.raiseNotImplementedError(ctx)

        pide.EnableOut.setValue(pide.EnableIn)

        if ctx.RungStatus:
            self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class IMC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)
    
    
@InstructionRegistry.register
class CC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)
    
@InstructionRegistry.register
class MMC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class RMPS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class POSP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class SRTP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class LDLG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class FGEN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class TOT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class DEDT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class D2SD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class D3SD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.raiseNotImplementedError(ctx)