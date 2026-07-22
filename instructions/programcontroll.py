import logging

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

@InstructionRegistry.register
class JMP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            ctx.Jump = self.args[0]

@InstructionRegistry.register
class LBL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pass

@InstructionRegistry.register
class TND(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ctx.TND = ctx.RungStatus

@InstructionRegistry.register
class MCR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ctx.inMCR = not ctx.inMCR

        if ctx.inMCR:
           if ctx.RungStatus:
                ctx.MCRActive = True
        else:
            ctx.MCRActive = False

@InstructionRegistry.register
class UID(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pass #TODO curently not needed
    
@InstructionRegistry.register
class UIE(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pass #TODO curently not needed

@InstructionRegistry.register
class AFI(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ctx.RungStatus = False

@InstructionRegistry.register
class NOP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        ctx.RungStatus = False
        ctx.RungEnabled = True

@InstructionRegistry.register
class JSR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            inputSize = int(self.args[1])
            inputArgs = self.args[2:2 + inputSize]

            val = []

            for key in inputArgs:
                val.append(self.getMemory(key))

            context = ExecutionContext(ProgramRef=ctx.ProgramRef, InputArgs=val)

            await ctx.ProgramRef.Routines[self.args[0]].execute(context)

            returnArgs = self.args[2 + inputSize:]

            for i, key in enumerate(returnArgs):
                if i < len(context.ReturnArgs):
                    self.setMemory(key, context.ReturnArgs[i])
    
@InstructionRegistry.register
class RET(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            if not ctx.Context.preScan and not ctx.Context.preScan :
                ctx.ReturnArgs = []
                for i, key in enumerate(self.args):
                    ctx.ReturnArgs.append(self.getMemory(key))
    
@InstructionRegistry.register
class SBR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        for i, key in enumerate(self.args):
            if i < len(ctx.InputArgs):
                self.setMemory(key, ctx.InputArgs[i])
    
@InstructionRegistry.register
class SFR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            name = self.args[0]
            ctx.ProgramRef.Routines[name].SFCStep = self.getMemory(self.args[1])
    
@InstructionRegistry.register
class SFP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            name = self.args[0]
            state = self.args[1]
            if state == 'Execute':
                ctx.ProgramRef.Routines[name].SFCPaused.setValue(0)
            else:
                ctx.ProgramRef.Routines[name].SFCPaused.setValue(1)
    
@InstructionRegistry.register
class EOT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.SFCTransition:
            if ctx.RungStatus:
                ctx.SFCStatus.setValue(self.getMemory(self.args[0]))
        else:
            ctx.RungStatus = False
            ctx.RungEnabled = True
    
@InstructionRegistry.register
class EVENT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        name = self.args[0]

        from core.emulator import Emulator
        from core.servicelocator import ServiceLocator
        emulator = ServiceLocator.get(Emulator)

        await emulator.tasks[name].execute(programs=emulator.programs, instruction=True)
