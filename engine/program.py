import logging

import engine.context

from contextlib import asynccontextmanager

from xml.etree.ElementTree import Element

from typing import Optional, Dict, TYPE_CHECKING, Any

from dataclasses import dataclass, field

from asyncua import Server

if TYPE_CHECKING:
    from core.memory.memory import Memory
    
from engine.routine import Routine

from core.xml.tags import loadTags
from core.timebase import getTimeMonotonic
from core.emulatorcontext import EmulatorContext

from opcua.tag import OpcuaTag
from opcua.mapping import Mapping

from datatypes.custom.numbers import SINT, DINT, INT
from datatypes.custom.array import Array
from datatypes.phase import PHASE

from engine.errors import MajorFault

from typing import ClassVar

@dataclass
class Program():
    _next_program_id: ClassVar[int] = 1

    _Element: Element = field(init=True)
    Name:str = field(init=True)
    server:Server = field(init=True)

    ID:int = field(init=False)
    phase:PHASE = field(init=False)

    Type:str = field(init=True, default=None)
    PreStateRoutineName:str = field(init=True, default=None)
    FaultRoutineName:str = field(init=True, default=None)
    TestEdits:bool = field(init=True, default=False)
    InitialStepIndex:INT = field(init=True, default_factory=INT)
    InitialState:str = field(init=True, default=None)
    CompleteStateIfNotImpl:str = field(init=True, default=None)
    LossOfCommCmd:str = field(init=True, default=None)
    ExternalRequestAction:str = field(init=True, default=None)
    UseAsFolder:bool = field(init=True, default=False)
    AutoValueAssignStepToPhase:bool = field(init=True, default=False)
    AutoValueAssignPhaseToStepOnComplete:bool = field(init=True, default=False)
    AutoValueAssignPhaseToStepOnStopped:bool = field(init=True, default=False)
    AutoValueAssignPhaseToStepOnAborted:bool = field(init=True, default=False)

    Routines: Dict[str, "Routine"] = field(init=False, default_factory=lambda: {})
    Class: Optional[str] = field(init=False, default=None)
    MainRoutineName: Optional[str] = field(init=False, default=None)
    memory:"Memory" = field(init=False)
    mapping:Mapping = field(init=False, default_factory=Mapping)
    opcua:OpcuaTag = field(init=False)

    DisableFlag:SINT = field(init=False, default_factory=SINT)
    LASTSCANTIME:DINT = field(init=False, default_factory=DINT)
    MAXSCANTIME:DINT = field(init=False, default_factory=DINT)
    MajorFaultRecord: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 11))
    MinorFaultRecord: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 11))

    def __post_init__(self):
        self.ID = Program._next_program_id
        Program._next_program_id += 1
        from core.memory.memory import Memory, PlcMemory

        self.memory = Memory(NAME=self.Name)
        PlcMemory.addContainer(self.memory)

        self.opcua = OpcuaTag(NAME=self.Name, SERVER=self.server)

        self.MainRoutineName = self._Element.get("MainRoutineName", None)
        self.Class = self._Element.get("Class", None)

    async def init(self):
        from engine.routine import Routine
        await self.opcua.registerNamespace(f"http://rockwell.plc/{self.Name}")
        await self.opcua.createFolder(f"Program:{self.Name}")

        await loadTags(self._Element, self.opcua, self.memory, self.mapping)

        await self.opcua.createNodes(self.memory, self.mapping)

        for routine in self._Element.findall("./Routines//Routine"):
            r = Routine(routine)
            self.Routines[r.Name] = r

        if self.Type == 'EquipmentPhase':
            from instructions.phase import PhaseStates, changeState
            from core.memory.helper import getMemory
            self.phase:PHASE = getMemory(self.Name)
            changeState(self.phase, self.InitialStepIndex, PhaseStates[self.InitialState])            

    @asynccontextmanager
    async def program_context(self):
        from engine.helper import CurrentProgramName
        token = CurrentProgramName.set(self.Name)
        try:
            yield
        #except STException as e:
        #    logging.exception(e)
        #    logging.exception(e.with_traceback(e.original_exception.__traceback__))
        except MajorFault as e:
            raise
        except Exception as e:
            logging.exception(e)
        finally:
            CurrentProgramName.reset(token)

    @asynccontextmanager
    async def program_time(self):
        start = getTimeMonotonic()
        try:
            yield
        finally:
            end = getTimeMonotonic()
            diff = end-start
            self.LASTSCANTIME.setValue(diff)

            if self.MAXSCANTIME < diff:
                self.MAXSCANTIME.setValue(diff)

    async def execute(self, context:EmulatorContext = None):
        if context is None:
            context = EmulatorContext()
        if self.DisableFlag == 0:
            if self.Type != 'EquipmentPhase':
                if self.MainRoutineName in self.Routines:
                    ctx = await self.run(self.MainRoutineName, context)
            else:
                '''
                from core.memory.helper import getMemory
                phase:PHASE = getMemory(self.Name)
                '''
                from instructions.phase import PhaseStates, changeState

                #if self.CurrentPhase == PhaseStates.Unchanged:
                #changeState(phase, self.InitialStepIndex, PhaseStates[self.InitialState])

                if self.PreStateRoutineName:
                    await self.run(self.PreStateRoutineName, context)

                PSC = PhaseStates.Unchanged
                if not self.phase.Paused:
                    if self.phase.Resetting:
                        ctx = await self.run('Resetting', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Idle
                    elif self.phase.Running:
                        ctx = await self.run('Running', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Complete
                    elif self.phase.Holding:
                        ctx = await self.run('Holding', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Held
                    elif self.phase.Restarting:
                        ctx = await self.run('Restarting', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Running
                    elif self.phase.Stopping:
                        ctx = await self.run('Stopping', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Stoppedz
                    elif self.phase.Aborting:
                        ctx = await self.run('Aborting', context)
                        if self.pcs('Resetting', ctx):
                            PSC = PhaseStates.Aborted

                    changeState(self.phase, self.InitialStepIndex, PSC)
        else:
            self.LASTSCANTIME.setValue(0)
            self.MAXSCANTIME.setValue(0)

    async def run(self, name:str, context:EmulatorContext = None) -> "engine.context.ExecutionContext":
        async with self.program_context(), self.program_time():
            from engine.context import ExecutionContext
            ctx = ExecutionContext(ProgramRef=self, Context=context)
            await self.Routines[name].execute(ctx=ctx)
            return ctx

    def pcs(self, name:str, ctx:"engine.context.ExecutionContext") -> bool:
        PSC = True
        if name in self.Routines:
            PSC = ctx.PSC

        return PSC