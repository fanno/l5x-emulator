from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class FPMS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class ESTOP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class ROUT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class RIN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class ENPIN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DIN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class LC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class THRS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCST(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCSTL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCSTM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCSRT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class SMAT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class TSAM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class TSSM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class FSBM(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class THRSe(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class CROUT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCA(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class DCAF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")