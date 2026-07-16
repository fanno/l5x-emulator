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

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        if ons.EnableIn:
            memory = ObjectRegistry.get(ons, ONSMemory)

            ons.OutputBit.setValue(False)
            if ons.InputBit:
                if not memory.ONS:
                    memory.ONS.setValue(True)
                    ons.OutputBit.setValue(True)
            else:
                memory.ONS.setValue(False)
        
        ons.EnableOut.setValue(ons.EnableIn)
    
@InstructionRegistry.register
class OSFI(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        ons:FBD_ONESHOT = self.getMemory(self.args[0])

        if ons.EnableIn:
            memory = ObjectRegistry.get(ons, ONSMemory)

            ons.OutputBit.setValue(False)
            if not ons.InputBit:
                if memory.ONS:
                    memory.ONS.setValue(False)
                    ons.OutputBit.setValue(True)
            else:
                memory.ONS.setValue(True)

        ons.EnableOut.setValue(ons.EnableIn)