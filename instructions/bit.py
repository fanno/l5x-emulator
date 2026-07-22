from dataclasses import dataclass, field

from engine.context import ExecutionContext
from engine.instruction import Instruction

from datatypes.fdb import FBD_ONESHOT
from datatypes.custom.bool import BOOL

from core.objectregistry import ObjectRegistry
from core.registry.instructionregistry import InstructionRegistry
from core.memory.identity import Identity

@dataclass
class ONSMemory(Identity):
    ONS:BOOL = field(init=False, default_factory=BOOL)

@InstructionRegistry.register
class OSRI(Instruction):
        
    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        memory = ObjectRegistry.get(ons, ONSMemory)

        memory.ONS.setValue(ons.InputBit)

        ons.EnableIn._reset()
        ons.EnableOut._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

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

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        memory = ObjectRegistry.get(ons, ONSMemory)

        memory.ONS.setValue(ons.InputBit)

        ons.EnableIn._reset()
        ons.EnableOut._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        if ons.EnableIn:
            memory = ObjectRegistry.get(ons, ONSMemory)

            ons.OutputBit.setValue(False)
            if not ons.InputBit:
                if memory.ONS:
                    ons.OutputBit.setValue(True)

            memory.ONS.setValue(ons.InputBit)

        ons.EnableOut.setValue(ons.EnableIn)