from engine.context import ExecutionContext

from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.memory.helper import OutputType
from datatypes.alarm import ALARM
from datatypes.pid import PID_ENHANCED


@InstructionRegistry.register
class ALM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        timer:ALARM = self.getMemory(self.args[0], OutputType.PLC)

        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class SCL(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        tag = self.args[0]

        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PIDE(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        pid:PID_ENHANCED = self.getMemory(self.args[0], OutputType.PLC)

        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class IMC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
    
@InstructionRegistry.register
class CC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class MMC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class RMPS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class POSP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SRTP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class LDLG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class FGEN(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class TOT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class DEDT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class D2SD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class D3SD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")