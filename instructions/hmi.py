from typing import Any
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.misc import HMIBC as HMIBCdt
from engine.fbd.block import FBDBlock

@InstructionRegistry.register
class HMIBC(Instruction):

    async def execute(self, alarm:HMIBCdt, ctx:"ExecutionContext") -> Any:
        self.raiseNotImplementedError(ctx)
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        value:HMIBC = self.getMemory(self.args[0])
        if ctx.RLL.RungStatus:
            self.execute(value, ctx)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        value:HMIBCdt = block.Value
        if value.EnableIn:
            self.execute(value, ctx)