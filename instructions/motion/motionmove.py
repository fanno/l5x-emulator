from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class MAS(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO        raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MAH(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO        raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MAJ(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MAM(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MAG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MCD(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MRP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MCCP(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        #TODO     raise NotImplementedError(f"{__class__} not implemented yet")
        pass

@InstructionRegistry.register
class MCSV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MAPC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MATC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class MDAC(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")