from typing import Dict, Any

from contextlib import asynccontextmanager

from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from engine.program import Program
from engine.helper import CurrentTaskName
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler
from engine.context import EmulatorContext
from engine.executiontimer import ExecutionTimer

from datatypes.custom.numbers import DINT, INT
from datatypes.custom.bool import BOOL
from datatypes.custom.dt import DT
from datatypes.custom.array import Array
from datatypes.custom.string import STRING

@dataclass
class EventInfo():
    _Element: Element = field(init=True)

    EventTrigger:STRING = field(init=False, default_factory=STRING)
    EnableTimeout:BOOL = field(init=False, default_factory=BOOL)
    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.EventTrigger = STRING(self._Element.get("EventTrigger", None))
            self.EnableTimeout = STRING(self._Element.get("EnableTimeout", None))

@dataclass
class Task():
    element: InitVar[Element | None]

    Name:str = field(init=False, default="")
    Class:str = field(init=False, default="")

    _programs:list[str] = field(init=False, default_factory=list)

    DisableUpdateOutputs:DINT = field(init=False, default_factory=DINT)
    EnableTimeOut:DINT = field(init=False, default_factory=DINT)
    InhibitTask:DINT = field(init=False, default_factory=DINT)
    Instance:DINT = field(init=False, default_factory=DINT)
    LastScanTime:DINT = field(init=False, default_factory=DINT)
    MaximumInterval: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 2))
    MaxScanTime:DINT = field(init=False, default_factory=DINT)
    MinimumInterval: Array[DINT] = field(init=False, default_factory=lambda: Array.create(DINT, 2))
    OverlapCount:DINT = field(init=False, default_factory=DINT)
    Priority:INT = field(init=False, default_factory=INT)
    Rate:DINT = field(init=False, default_factory=DINT)
    StartTime:DT = field(init=False, default_factory=DT)
    Status:DINT = field(init=False, default_factory=DINT)
    Watchdog:DINT = field(init=False, default_factory=DINT)
    scanCount:int = 0
    _lastRun:DT = field(init=False, default_factory=DT)

    EventInfo:"EventInfo" = field(init=False, default_factory=DINT)

    RateDT:DT = None
    def __post_init__(self, element: Element):
        if isinstance(element, Element):
            self.Name = element.get("Name", None)
            self.Class = element.get("Class", None)
            self.Type = element.get("Type", None)

            self.Rate = DINT(element.get("Rate", 0)) * 1000
            self.RateDT = DT(self.Rate.getPLCValue())

            self.Priority = DINT(element.get("Priority", 0))
            self.Watchdog = DINT(element.get("Watchdog", 0)) * 1000

            if BOOL(element.get("DisableUpdateOutputs", False)):
                self.DisableUpdateOutputs.setValue(1)
            else:
                self.DisableUpdateOutputs.setValue(0)

            if BOOL(element.get("InhibitTask", False)):
                self.InhibitTask.setValue(1)
            else:
                self.InhibitTask.setValue(0)

            for program in element.findall("./ScheduledPrograms//ScheduledProgram"):
                self._programs.append(program.get("Name", None))

            self.EventInfo = EventInfo(element.find("./EventInfo"))

    @asynccontextmanager
    async def task_context(self):
        token = CurrentTaskName.set(self.Name)
        try:
            yield
        finally:
            CurrentTaskName.reset(token)

    async def execute(self, programs:Dict[str, Program], instruction:bool = False):
        with Hierarchy.scope(self.Name):
            with PLCFaultHandler.minor():
                if self.InhibitTask == 0:
                    self.StartTime = DT()

                    run = False
                    emulator = EmulatorContext.get()
                    
                    if emulator.preScan or emulator.postScan:
                        run = True

                    if not run:
                        if self.Type == "CONTINUOUS":
                            run = True
                        elif self.Type == "PERIODIC":
                            if self._lastRun == 0 or self.RateDT < self.StartTime - self._lastRun:
                                run = True
                        elif self.Type == "EVENT":
                            if self.EventInfo.EventTrigger == 'EVENT Instruction Only':
                                if instruction:
                                    run = True
                        if run:
                            self._lastRun = self.StartTime
                    if run:
                        timer = ExecutionTimer()
                        with timer:
                            async with self.task_context():
                                for program in self._programs:
                                    await programs[program].execute()

                        self.LastScanTime.setValue(timer.μs)
                        if self.MaxScanTime < timer.μs:
                            self.MaxScanTime.setValue(timer.μs)
                        if not emulator.preScan and not emulator.postScan:
                            self.scanCount += 1