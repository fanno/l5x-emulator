from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.errors import MajorFault

from core.registry.instructionregistry import InstructionRegistry

from  instructions.helper import getPLCValue
from datatypes.phase import PHASE

from enum import Enum, auto

class PhaseStates(Enum):
    Unchanged = auto()
    Resetting = auto()
    Running = auto()
    Holding = auto()
    Restarting = auto()
    Stopping = auto()
    Aborting = auto()
    Idle = auto()
    Held = auto()
    Complete = auto()
    Stopped = auto()
    Aborted = auto()

def changeState(phase:PHASE, ínit:int, state:PhaseStates = PhaseStates.Unchanged):
    if state is not PhaseStates.Unchanged:
        phase.Resetting._reset()
        phase.Running._reset()
        phase.Holding._reset()
        phase.Restarting._reset()
        phase.Stopping._reset()
        phase.Aborting._reset()
        phase.Idle._reset()
        phase.Held._reset()
        phase.Complete._reset()
        phase.Stopped._reset()
        phase.Aborted._reset()

        phase.StepIndex.setValue(ínit)

        match state:
            case PhaseStates.Resetting:
                phase.Resetting.setValue(True)
            case PhaseStates.Running:
                phase.Running.setValue(True)
            case PhaseStates.Holding:
                phase.Holding.setValue(True)
            case PhaseStates.Restarting:
                phase.Restarting.setValue(True)
            case PhaseStates.Stopping:
                phase.Stopping.setValue(True)
            case PhaseStates.Aborting:
                phase.Aborting.setValue(True)
            case PhaseStates.Idle:
                phase.Idle.setValue(True)
            case PhaseStates.Held:
                phase.Held.setValue(True)
            case PhaseStates.Complete:
                phase.Complete.setValue(True)
            case PhaseStates.Stopped:
                phase.Stopped.setValue(True)
            case PhaseStates.Aborted:
                phase.Aborted.setValue(True)


@InstructionRegistry.register
class PSC(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.ProgramRef.Type != 'EquipmentPhase':
            raise MajorFault(4, 91)

        if ctx.RungStatus:
            ctx.PSC = True
    
@InstructionRegistry.register
class PFL(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.ProgramRef.Type != 'EquipmentPhase':
            raise MajorFault(4, 91)
        
        if ctx.RungStatus:
            code = getPLCValue(self.getMemory(self.args[0]))

            phase:PHASE = self.getMemory(ctx.ProgramRef.Name)

            if code > phase.Failure:
                phase.Failure.setValue(code)
    
@InstructionRegistry.register
class PXRQ(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")
    
@InstructionRegistry.register
class PPD(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.ProgramRef.Type != 'EquipmentPhase':
            raise MajorFault(4, 91)
            
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(ctx.ProgramRef.Name)
            print("PPD: ladder_execute")
            if phase.PauseEnabled:
                phase.Paused.setValue(True)
    
@InstructionRegistry.register
class PCMD(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(self.args[0])
            command:str = self.args[1]
            result = self.getMemory(self.args[2])

            resultCode = 0
            invalidCode = 24578

            if phase.Owner == 0 or phase.Owner == ctx.ProgramRef.ID:
                match command:
                    case 'Reset':
                        if phase.Complete or phase.Stopped or phase.Aborted:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Resetting)
                        else:
                            resultCode = invalidCode
                    case 'Start':
                        if phase.Idle:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Running)
                        else:
                            resultCode = invalidCode
                    case 'Hold':
                        if phase.Running or phase.Restarting:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Holding)
                        else:
                            resultCode = invalidCode
                    case 'Restart':
                        if phase.Held:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Restarting)
                        else:
                            resultCode = invalidCode
                    case 'Stop':
                        if phase.Resetting or phase.Idle or phase.Running or phase.Holding or phase.Restarting or phase.Held:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Stopping)
                        else:
                            resultCode = invalidCode
                    case 'Abort':
                        if phase.Resetting or phase.Idle or phase.Running or phase.Holding or phase.Restarting or phase.Held or phase.Stopping:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Aborting)
                        else:
                            resultCode = invalidCode
                    case 'Reset':
                        if phase.Complete or phase.Stopped or phase.Aborted:
                            changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Restarting)
                        else:
                            resultCode = invalidCode
                    case 'AutoPause':
                        phase.AutoPauseEnabled.setValue(not phase.AutoPauseEnabled)
                    case 'Pause':
                        phase.PauseEnabled.setValue(True)
                    case 'Resume':
                        if not phase.AutoPauseEnabled:
                            phase.PauseEnabled._reset()

                        phase.Paused.setValue(False)
            else:
                resultCode = 24579

            result.setValue(resultCode)
    
@InstructionRegistry.register
class POVR(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(self.args[0])
            command:str = self.args[1]
            result = self.getMemory(self.args[2])

            resultCode = 0

            invalidCode = 24578

            match command:
                case 'Abort':
                    if phase.Resetting or phase.Idle or phase.Running or phase.Holding or phase.Restarting or phase.Held or phase.Stopping:
                        changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Aborting)
                    else:
                        resultCode = invalidCode
                case 'Stop':
                    if phase.Resetting or phase.Idle or phase.Running or phase.Holding or phase.Restarting or phase.Held:
                        changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Stopping)
                    else:
                        resultCode = invalidCode
                case 'Hold':
                    if phase.Running or phase.Restarting:
                        changeState(phase, ctx.ProgramRef.InitialStepIndex, PhaseStates.Holding)
                    else:
                        resultCode = invalidCode

            result.setValue(resultCode)
    
@InstructionRegistry.register
class PCLF(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(self.args[0])

            phase.Failure._reset()
    
@InstructionRegistry.register
class PRNP(Instruction):
    
    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.ProgramRef.Type != 'EquipmentPhase':
            raise MajorFault(4, 91)
        
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(ctx.ProgramRef.Name)

            phase.NewInputParameters._reset()

@InstructionRegistry.register
class PATT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(self.args[0])
            result = self.getMemory(self.args[2])

            if phase.Owner == ctx.ProgramRef.ID:
                resultCode = 24582
            elif phase.Owner != 0:
                resultCode = 24593
            else:
                resultCode = 0
                phase.Owner.setValue(ctx.ProgramRef.ID)

            result.setValue(resultCode)

@InstructionRegistry.register
class PDET(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            phase:PHASE = self.getMemory(self.args[0])

            phase.Owner._reset()