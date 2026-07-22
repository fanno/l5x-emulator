from engine.context import ExecutionContext
from engine.instruction import Instruction

from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class PSC(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PFL(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PXRQ(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PPD(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PRCP(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
    
@InstructionRegistry.register
class PCMD(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
    
@InstructionRegistry.register
class PCLF(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PRNP(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PDET(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class POVR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")