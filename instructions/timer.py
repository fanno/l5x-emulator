from dataclasses import dataclass, field
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.objectregistry import ObjectRegistry
from core.memory.identity import Identity
from datatypes.misc import TIMER, COUNTER
from datatypes.fdb import FBD_TIMER, FBD_COUNTER
from datatypes.custom.numbers import DINT

from typing import Any

from engine.fbd.block import FBDBlock

@dataclass
class TimerMemory(Identity):
    LAST_TIME:DINT = field(init=False, default_factory=DINT)

@InstructionRegistry.register
class TON(Instruction):

    async def ladder_preScan(self, ctx):
        timer:TIMER = self.getMemory(self.args[0])
        ObjectRegistry.remove(timer)

        timer.EN._reset()
        timer.TT._reset()
        timer.DN._reset()
        timer.ACC._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> TIMER:
        timer:TIMER = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(timer, TimerMemory)

        timer.EN.setValue(ctx.RLL.RungStatus)
        
        if not ctx.RLL.RungStatus:
            memory.LAST_TIME.setValue(0)
            timer.ACC.setValue(0)
        else:
            now = ctx.Time.now_ms()
            if memory.LAST_TIME == 0:
                memory.LAST_TIME = now
            elif timer.PRE > timer.ACC:
                timer.ACC.setValue(now - memory.LAST_TIME)

        timer.TT.setValue((timer.ACC <= timer.PRE) and timer.EN)
        timer.DN.setValue((timer.ACC >= timer.PRE) and timer.EN)
        return timer
        
@InstructionRegistry.register
class TOF(Instruction):

    async def ladder_preScan(self, ctx):
        timer:TIMER = self.getMemory(self.args[0])
        ObjectRegistry.remove(timer)

        timer.EN._reset()
        timer.TT._reset()
        timer.DN._reset()
        timer.ACC.setValue(timer.PRE)

    async def ladder_execute(self, ctx:"ExecutionContext") -> TIMER:
        timer:TIMER = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(timer, TimerMemory)

        if ctx.RLL.RungStatus:
            timer.EN.setValue(True)
            timer.DN.setValue(True)
            timer.TT.setValue(False)
            memory.LAST_TIME.setValue(0)
            timer.ACC.setValue(0)
        else:
            now = ctx.Time.now_ms()
            if memory.LAST_TIME == 0:
                memory.LAST_TIME = now
            elif timer.PRE > timer.ACC:
                timer.ACC.setValue(now - memory.LAST_TIME)
        
        timer.TT.setValue((timer.ACC <= timer.PRE) and not timer.EN)
        timer.DN.setValue((timer.ACC <= timer.PRE) and not timer.EN)

        return timer
        
@InstructionRegistry.register
class RTO(Instruction):

    async def ladder_preScan(self, ctx):
        timer:TIMER = self.getMemory(self.args[0])
        ObjectRegistry.remove(timer)

        timer.EN._reset()
        timer.TT._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> TIMER:
        timer:TIMER = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(timer, TimerMemory)

        timer.EN.setValue(ctx.RLL.RungStatus)
        
        if not ctx.RLL.RungStatus:
            memory.LAST_TIME.setValue(0)
            timer.TT.setValue(False)
        else:
            now = ctx.Time.now_ms()
            if memory.LAST_TIME == 0:
                memory.LAST_TIME = now
            if now > memory.LAST_TIME:
                if not timer.DN:
                    timer.ACC += now - memory.LAST_TIME
                    memory.LAST_TIME = now

        timer.DN.setValue((timer.ACC >= timer.PRE) and timer.ACC > 0)
        timer.TT.setValue((not timer.DN) and timer.EN)

        return timer

@InstructionRegistry.register
class TONR(Instruction):

    def preScan(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> None:
        timer.EnableIn._reset()
        timer.EnableOut._reset()

    def execute(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> Any:
        memory = ObjectRegistry.get(timer, TimerMemory)

        if timer.EnableIn:
            timer.EN.setValue(timer.TimerEnable and not timer.Reset)

            timer.Status.setValue(0)
            timer.InstructFault.setValue(False)
            timer.PresetInv.setValue(False)
            if timer.EN:
                now = ctx.Time.now_ms()
                if memory.LAST_TIME == 0:
                    memory.LAST_TIME = now
                elif timer.PRE > timer.ACC:
                    timer.ACC += (now - memory.LAST_TIME)
                    memory.LAST_TIME = now

            if not timer.EN or timer.Reset:
                memory.LAST_TIME.setValue(0)
                timer.ACC.setValue(0)

            timer.TT.setValue((timer.ACC <= timer.ACC) and timer.EN)
            timer.DN.setValue((timer.ACC >= timer.PRE) and timer.EN)

        timer.EnableOut.setValue(timer.EnableIn)

@InstructionRegistry.register
class TOFR(Instruction):

    def preScan(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> None:
        timer.EnableIn._reset()
        timer.EnableOut._reset()

    def execute(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> Any:
        memory = ObjectRegistry.get(timer, TimerMemory)

        if timer.EnableIn:
            timer.EN.setValue(timer.TimerEnable or timer.Reset)

            timer.Status.setValue(0) #TODO
            timer.InstructFault.setValue(False) #TODO
            timer.PresetInv.setValue(False) #TODO
            if not timer.EN:
                now = ctx.Time.now_ms()
                if memory.LAST_TIME == 0:
                    memory.LAST_TIME = now
                elif timer.PRE > timer.ACC:
                    timer.ACC += (now - memory.LAST_TIME)
                    timer.ACC.setValue(timer.ACC + (now - memory.LAST_TIME))
                    memory.LAST_TIME = now

            if timer.EN or timer.Reset:
                memory.LAST_TIME.setValue(0)
                timer.ACC.setValue(0)

            timer.TT.setValue((timer.ACC <= timer.PRE) and not timer.EN)
            timer.DN.setValue((timer.ACC <= timer.PRE) and not timer.EN)

        timer.EnableOut.setValue(timer.EnableIn)
        return timer

@InstructionRegistry.register
class RTOR(Instruction):

    def preScan(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> None:
        timer.EnableIn._reset()
        timer.EnableOut._reset()

    def execute(self, timer:FBD_TIMER, ctx:"ExecutionContext") -> Any:
        memory = ObjectRegistry.get(timer, TimerMemory)

        if timer.EnableIn:
            timer.EN.setValue(timer.TimerEnable)

            timer.Status.setValue(0)
            timer.InstructFault.setValue(False)
            timer.PresetInv.setValue(False)
            if timer.EN:
                now = ctx.Time.now_ms()
                if memory.LAST_TIME == 0:
                    memory.LAST_TIME = now
                elif timer.PRE > timer.ACC:
                    timer.ACC += (now - memory.LAST_TIME)
                    memory.LAST_TIME = now
            else:
                memory.LAST_TIME.setValue(0)

            if timer.Reset:
                memory.LAST_TIME.setValue(0)
                timer.ACC.setValue(0)

            timer.TT.setValue((timer.ACC <= timer.PRE) and timer.EN)
            timer.DN.setValue((timer.ACC >= timer.PRE) and timer.EN)

            timer.ACC.setValue(timer.ACC)

        timer.EnableOut.setValue(timer.EnableIn)

        return timer

@InstructionRegistry.register
class RES(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> TIMER|COUNTER|None:
        ref = self.getMemory(self.args[0])

        if ref.__class__.__name__ == "TIMER":
            timer:TIMER = ref
            memory = ObjectRegistry.get(timer, TimerMemory)
            timer.ACC.setValue(0)
            timer.DN.setValue(False)
            timer.TT.setValue(False)
            timer.EN.setValue(False)
            memory.LAST_TIME.setValue(0)
            
            return timer
        elif ref.__class__.__name__ == "COUNTER":
            counter:COUNTER = ref
            counter.ACC.setValue(0)
            counter.CU.setValue(False)
            counter.CD.setValue(False)
            counter.DN.setValue(False)
            counter.OV.setValue(False)
            counter.UN.setValue(False)

            return counter

@InstructionRegistry.register
class CTU(Instruction):

    async def ladder_preScan(self, ctx):
        counter:COUNTER = self.getMemory(self.args[0])

        counter.CU.setValue(True)  

    async def ladder_execute(self, ctx:"ExecutionContext") -> COUNTER:
        counter:COUNTER = self.getMemory(self.args[0])

        counter.CU.setValue(ctx.RLL.RungStatus)

        if ctx.RLL.RungStatus and not counter.OV:
            counter.ACC += 1

        counter.OV.setValue(counter.ACC >= 2147483647)
        counter.UN.setValue(counter.ACC <= -2147483648)
        counter.DN.setValue(counter.ACC >= counter.PRE)

        return counter

@InstructionRegistry.register
class CTD(Instruction):

    async def ladder_preScan(self, ctx):
        counter:COUNTER = self.getMemory(self.args[0])

        counter.CD.setValue(True)      

    async def ladder_execute(self, ctx:"ExecutionContext") -> COUNTER:
        counter:COUNTER = self.getMemory(self.args[0])

        counter.CU.setValue(ctx.RLL.RungStatus)

        if ctx.RLL.RungStatus and not counter.UN:
            counter.ACC -= 1

        counter.OV.setValue(counter.ACC >= 2147483647)
        counter.UN.setValue(counter.ACC <= -2147483648)
        counter.DN.setValue(counter.ACC <= counter.PRE)

        return counter

@InstructionRegistry.register
class CTUD(Instruction):

    def preScan(self, counter:FBD_COUNTER, ctx:"ExecutionContext"):
        counter.EnableIn._reset()
        counter.EnableOut._reset()

    def execute(self, counter:FBD_COUNTER, ctx:"ExecutionContext") -> Any:
        if counter.EnableIn:
            if counter.CUEnable and not counter.CU:
                counter.ACC += 1

            if counter.CDEnable and not counter.CD:
                counter.ACC -= 1

            counter.CU.setValue(counter.CUEnable)
            counter.CD.setValue(counter.CDEnable)

            if counter.Reset:
                counter.ACC.setValue(0)

            counter.OV.setValue(counter.ACC >= 2147483647)
            counter.UN.setValue(counter.ACC <= -2147483648)
            counter.DN.setValue(counter.ACC >= counter.PRE)
        counter.EnableOut.setValue(counter.EnableIn)
        return counter
    
    async def fbd_preScan(self, ctx:"ExecutionContext", block:FBDBlock):
        counter:FBD_COUNTER = block.Value

        counter.EnableIn._reset()
        counter.EnableOut._reset()