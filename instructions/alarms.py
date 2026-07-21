from engine.context import ExecutionContext

from dataclasses import dataclass, field

from engine.instruction import Instruction

from core.registry.instructionregistry import InstructionRegistry
from core.memory.memory import Memory
from core.memory.identity import Identity
from core.objectregistry import ObjectRegistry

from datatypes.alarm import ALARM_DIGITAL, ALARM_ANALOG, ALARM_SET_CONTROL, ALARM_SET
from datatypes.custom.numbers import DINT, REAL, INTIGER
from datatypes.custom.bool import BOOL
from datatypes.misc import TIMER

from instructions.timer import TON

@dataclass
class AlarmMemory(Identity):
    memory:Memory = field(init=False, default_factory=lambda: Memory(NAME="local"))

@dataclass
class ALMDMemory(AlarmMemory):
    timer:TON = None

    ProgAckONS:BOOL = field(init=False, default_factory=BOOL)
    ProgResetONS:BOOL = field(init=False, default_factory=BOOL)

    def __post_init__(self):
        self.memory.set("MinDuration", TIMER())

        self.timer = TON(args=["MinDuration"], memory=self.memory)

    def setMinDuration(self, MinDurationPRE:DINT):
        timer:TIMER = self.memory.get("MinDuration")
        timer.PRE.setValue(MinDurationPRE) 

@InstructionRegistry.register
class ALMD(Instruction):

    async def preScan(self, ctx):
        await super().preScan(ctx)
        alarm:ALARM_DIGITAL = self.getMemory(self.args[0])
        ObjectRegistry.remove(alarm)
        
        alarm._reset()
        alarm.Acked.setValue(True)

    async def execute(self, ctx:"ExecutionContext") -> None:
        alarm:ALARM_DIGITAL = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(alarm, ALMDMemory)

        ProgAck:BOOL = self.getMemory(self.args[1])
        ProgReset:BOOL = self.getMemory(self.args[2])
        ProgDisable:BOOL = self.getMemory(self.args[3])
        ProgEnable:BOOL = self.getMemory(self.args[4])

        alarm.ProgAck.setValue(ProgAck)
        alarm.ProgReset.setValue(ProgReset)
        alarm.ProgDisable.setValue(ProgDisable) #TODO USE ?
        alarm.ProgEnable.setValue(ProgEnable) #TODO USE ?
        
        memory.setMinDuration(alarm.MinDurationPRE)

        ProgAck = alarm.ProgAck and not memory.ProgAckONS
        memory.ProgAckONS.setValue(alarm.ProgAck)
        ProgReset = alarm.ProgReset and not memory.ProgResetONS
        memory.ProgResetONS.setValue(alarm.ProgReset)
 
        isInAlarm = False
        if not alarm.OperDisable or alarm.OperEnable:
            if not alarm.ProgDisable or alarm.ProgEnable:
                isInAlarm = alarm.In == alarm.Condition

        timer = await memory.timer.execute(ExecutionContext(RungStatus=isInAlarm))

        if isInAlarm:
            if timer.DN:
                if not alarm.InAlarm:
                    alarm.InAlarm.setValue(True)

                    alarm.AlarmCount.setValue( alarm.AlarmCount + 1 )

                    if alarm.AckRequired:
                        alarm.Acked.setValue(False)

        if alarm.AckRequired:
            if alarm.Latched:
                if alarm.InAlarm:
                    if ProgAck or alarm.OperAck:
                        alarm.Acked.setValue(True)

                if not isInAlarm:
                    if ProgReset or alarm.OperReset:
                        alarm.InAlarm.setValue(False)
                        alarm.Acked.setValue(True)
            else:
                if ProgAck or alarm.OperAck:
                    alarm.Acked.setValue(True)

                if not isInAlarm:
                    alarm.InAlarm.setValue(False)
        else:
            if alarm.InAlarm:
                alarm.Acked.setValue(True)

            if alarm.Latched:
                if not isInAlarm:
                    if ProgReset or alarm.OperReset:
                        alarm.InAlarm.setValue(False)
            else:
                if not isInAlarm:
                    alarm.InAlarm.setValue(False)

        if alarm.AlarmCountReset:
            alarm.AlarmCount.setValue(0)

        alarm.OperAck.setValue(False)
        alarm.OperReset.setValue(False)
        alarm.AlarmCountReset.setValue(False)

        alarm.MinDurationACC.setValue(0)

@dataclass
class ALMAMemory(AlarmMemory):
    HHTimer:TON = None
    HTimer:TON = None
    LTimer:TON = None
    LLTimer:TON = None

    def __post_init__(self):
        self.memory.set("HHTimer", TIMER())
        self.memory.set("HTimer", TIMER())
        self.memory.set("LTimer", TIMER())
        self.memory.set("LLTimer", TIMER())

        self.HHTimer = TON(args=["HHTimer"], memory=self.memory)
        self.HTimer = TON(args=["HTimer"], memory=self.memory)
        self.LTimer = TON(args=["LTimer"], memory=self.memory)
        self.LLTimer = TON(args=["LLTimer"], memory=self.memory)

    def setMinDuration(self, MinDurationPRE:DINT):
        HHTimer:TIMER = self.memory.get("HHTimer")
        HHTimer.PRE.setValue(MinDurationPRE)
        HTimer:TIMER = self.memory.get("HTimer")
        HTimer.PRE.setValue(MinDurationPRE)
        LTimer:TIMER = self.memory.get("LTimer")
        LTimer.PRE.setValue(MinDurationPRE)
        LLTimer:TIMER = self.memory.get("LLTimer")
        LLTimer.PRE.setValue(MinDurationPRE)                        

@InstructionRegistry.register
class ALMA(Instruction):

    async def preScan(self, ctx):
        await super().preScan(ctx)
        alarm:ALARM_ANALOG = self.getMemory(self.args[0])
        ObjectRegistry.remove(alarm)
        
        alarm.reset()

    async def execute(self, ctx:"ExecutionContext") -> None:
        alarm:ALARM_ANALOG = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(alarm, ALMAMemory)

        In:REAL|INTIGER = self.getMemory(self.args[1])
        ProgAckALL:BOOL = self.getMemory(self.args[2])
        ProgDisable:BOOL = self.getMemory(self.args[3])
        ProgEnable:BOOL = self.getMemory(self.args[4])

        alarm.ProgDisable.setValue(ProgDisable) #TODO USE ?
        alarm.ProgEnable.setValue(ProgEnable) #TODO USE ?

        memory.setMinDuration(alarm.MinDurationPRE)

        isInHHAlarm = False
        isInHAlarm = False
        isInLAlarm = False
        isInLLAlarm = False
        if not alarm.OperDisable or alarm.OperEnable:
            if not alarm.ProgDisable or alarm.ProgEnable:
                isInHHAlarm = alarm.HEnabled and In > alarm.HLimit
                isInHAlarm = alarm.HEnabled and In > alarm.HLimit
                isInLAlarm = alarm.LEnabled and In < alarm.LLimit
                isInLLAlarm = alarm.LLEnabled and In < alarm.LLLimit

        HHTimer = await memory.HHTimer.execute(ExecutionContext(RungStatus=isInHHAlarm))
        HTimer = await memory.HTimer.execute(ExecutionContext(RungStatus=isInHAlarm))
        LTimer = await memory.LTimer.execute(ExecutionContext(RungStatus=isInLAlarm))
        LLTimer = await memory.LLTimer.execute(ExecutionContext(RungStatus=isInLLAlarm))

        if HHTimer.DN:
            if not alarm.HHInAlarm:
                alarm.HHAlarmCount.setValue( alarm.HHAlarmCount + 1 )
            alarm.HHInAlarm.setValue(True)
        if HTimer.DN:
            if not alarm.HHInAlarm:
                alarm.HAlarmCount.setValue( alarm.HAlarmCount + 1 )            
            alarm.HHInAlarm.setValue(True)
        if LTimer.DN:
            if not alarm.HHInAlarm:
                alarm.LAlarmCount.setValue( alarm.LAlarmCount + 1 )
            alarm.LInAlarm.setValue(True)
        if LLTimer.DN:
            if not alarm.HHInAlarm:
                alarm.LLAlarmCount.setValue( alarm.LLAlarmCount + 1 )
            alarm.LLInAlarm.setValue(True)

        if not alarm.AckRequired:
            if alarm.HHInAlarm:
                if In < (alarm.HHLimit - alarm.Deadband):
                    alarm.HHInAlarm.setValue(False)
                    alarm.HHAcked.setValue(True)
            if alarm.HInAlarm:
                if In < (alarm.HLimit - alarm.Deadband):
                    alarm.HInAlarm.setValue(False)
                    alarm.HAcked.setValue(True)
            if alarm.LInAlarm:
                if In < (alarm.LLimit + alarm.Deadband):
                    alarm.LInAlarm.setValue(False)
                    alarm.LAcked.setValue(True)
            if alarm.LLInAlarm:
                if In < (alarm.LLLimit + alarm.Deadband):
                    alarm.LLInAlarm.setValue(False)
                    alarm.LLAcked.setValue(True)
        else:
            if not alarm.HHAcked:
                if alarm.HHProgAck or alarm.HHOperAck:
                    alarm.HHAcked.setValue(True)
            if not alarm.HAcked:
                if alarm.HProgAck or alarm.HOperAck:
                    alarm.HAcked.setValue(True)
            if not alarm.LAcked:
                if alarm.LProgAck or alarm.LOperAck:
                    alarm.LAcked.setValue(True)
            if not alarm.LLAcked:
                if alarm.LLProgAck or alarm.LLOperAck:
                    alarm.LLAcked.setValue(True)

        if alarm.ROC >= alarm.ROCPosLimit:
            alarm.ROCPosInAlarm.setValue(True)
            alarm.ROCPosAcked.setValue(False)
        else:
            alarm.ROCPosInAlarm.setValue(False)
        if not alarm.ROCPosAcked:
            if alarm.ROCPosProgAck or alarm.ROCPosOperAck:
                alarm.ROCPosAcked.setValue(True)

        if alarm.ROC <= alarm.ROCNegLimit:
            alarm.ROCNegInAlarm.setValue(True)
            alarm.ROCNegAcked.setValue(False)
        else:
            alarm.ROCNegInAlarm.setValue(False)
        if not alarm.ROCNegAcked:
            if alarm.ROCNegProgAck or alarm.ROCNegOperAck:
                alarm.ROCNegAcked.setValue(True)

        if alarm.AlarmCountReset:
            alarm.HHAlarmCount.setValue(0)
            alarm.HAlarmCount.setValue(0)
            alarm.LAlarmCount.setValue(0)
            alarm.LLAlarmCount.setValue(0)

        alarm.HHOperAck.setValue(False)
        alarm.HOperAck.setValue(False)
        alarm.LOperAck.setValue(False)
        alarm.LLOperAck.setValue(False)
        alarm.HHProgAck.setValue(False)
        alarm.HProgAck.setValue(False)
        alarm.LProgAck.setValue(False)
        alarm.LLProgAck.setValue(False)
        alarm.ROCPosProgAck.setValue(False)
        alarm.ROCPosOperAck.setValue(False)
        alarm.ROCNegProgAck.setValue(False)
        alarm.ROCNegOperAck.setValue(False)
        alarm.AlarmCountReset.setValue(False)

        alarm.MinDurationACC.setValue(0)

@InstructionRegistry.register
class ASO(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        AlarmSet:ALARM_SET = self.getMemory(self.args[0])
        Control:ALARM_SET_CONTROL = self.getMemory(self.args[1])

        if ctx.RungStatus:
            if not Control.LastState:
                Operation = self.args[2]

                match Operation:
                    case "Acknowledge":
                        AlarmSet.InAlarmAckedCount.setValue(AlarmSet.InAlarmAckedCount.getPLCValue() + 1)
                    case "Reset":
                        raise NotImplementedError(f"{__class__} {Operation} not implemented yet")
                    case "Enable":
                        raise NotImplementedError(f"{__class__} {Operation} not implemented yet")
                    case "Disable":
                        AlarmSet.DisabledCount.setValue(AlarmSet.DisabledCount.getPLCValue() + 1)
                    case "Unshelve":
                        raise NotImplementedError(f"{__class__} {Operation} not implemented yet")
                    case "Suppress":
                        AlarmSet.SuppressedCount.setValue(AlarmSet.SuppressedCount.getPLCValue() + 1)
                    case "Unsuppress":
                        raise NotImplementedError(f"{__class__} {Operation} not implemented yet")
                    case "ResetAlarmCount":
                        AlarmSet._reset()
                    case _:
                        raise NotImplementedError(f"{__class__} {Operation} not implemented yet")
        
        Control.LastState.setValue(Control.LastState)