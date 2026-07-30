from dataclasses import dataclass, field

from engine.context import ExecutionContext
from engine.instruction import Instruction

from datatypes.fdb import FBD_ONESHOT
from datatypes.custom.bool import BOOL

from core.objectregistry import ObjectRegistry
from core.registry.instructionregistry import InstructionRegistry
from core.memory.identity import Identity
from typing import Any
from engine.fbd.block import FBDBlock

@dataclass
class ONSMemory(Identity):
    ONS:BOOL = field(init=False, default_factory=BOOL)

@InstructionRegistry.register
class OSRI(Instruction):

    async def preScan(self, ons:FBD_ONESHOT, ctx:"ExecutionContext"):
        memory = ObjectRegistry.get(ons, ONSMemory)

        memory.ONS.setValue(ons.InputBit)

        ons.EnableIn._reset()
        ons.EnableOut._reset()

    async def execute(self, ons:FBD_ONESHOT, ctx:"ExecutionContext") -> Any:
        if ons.EnableIn:
            memory = ObjectRegistry.get(ons, ONSMemory)

            ons.OutputBit.setValue(False)
            if ons.InputBit:
                if not memory.ONS:
                    ons.OutputBit.setValue(True)
            
            memory.ONS.setValue(ons.InputBit)
        
        ons.EnableOut.setValue(ons.EnableIn)
    
@InstructionRegistry.register
class OSFI(Instruction):

    async def preScan(self, ons:FBD_ONESHOT, ctx:"ExecutionContext"):
        memory = ObjectRegistry.get(ons, ONSMemory)

        memory.ONS.setValue(ons.InputBit)

        ons.EnableIn._reset()
        ons.EnableOut._reset()

    async def execute(self, ons:FBD_ONESHOT, ctx:"ExecutionContext") -> Any:
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        if ons.EnableIn:
            memory = ObjectRegistry.get(ons, ONSMemory)

            ons.OutputBit.setValue(False)
            if not ons.InputBit:
                if memory.ONS:
                    ons.OutputBit.setValue(True)

            memory.ONS.setValue(ons.InputBit)

        ons.EnableOut.setValue(ons.EnableIn)

@InstructionRegistry.register
class XIC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= bool(self.getMemory(self.args[0]))

@InstructionRegistry.register
class XIO(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.RungStatus &= not bool(self.getMemory(self.args[0]))

@InstructionRegistry.register
class OTE(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        self.setMemory(self.args[0], ctx.RungStatus)

@InstructionRegistry.register
class OTL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dest = self.getMemory(self.args[0])
            dest.setValue(True)

@InstructionRegistry.register
class OTU(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            dest = self.getMemory(self.args[0])
            dest.setValue(False)

@InstructionRegistry.register
class ONS(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])

        ons.setValue(ctx.RungStatus)
        if ons and ctx.RungStatus:
            ctx.RungStatus = False

@InstructionRegistry.register
class OSR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])
        out = self.getMemory(self.args[1])

        out.setValue(False)
        if ctx.RungStatus:
            if not ons:
                out.setValue(True)
        ons.setValue(ctx.RungStatus)
        
@InstructionRegistry.register
class OSF(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ons = self.getMemory(self.args[0])
        out = self.getMemory(self.args[1])

        out.setValue(False)
        if not ctx.RungStatus:
            if ons:
                out.setValue(True)
        ons.setValue(ctx.RungStatus)