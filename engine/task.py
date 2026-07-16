import logging

import time

from contextlib import asynccontextmanager

from xml.etree.ElementTree import Element

from typing import Dict

from dataclasses import dataclass, field

from asyncua import ua

from engine.program import Program
from engine.helper import CurrentTaskName

from core.timebase import getTimeMonotonic

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
        if self._Element is not None:
            self.EventTrigger = STRING(self._Element.get("EventTrigger", None))
            self.EnableTimeout = STRING(self._Element.get("EnableTimeout", None))

@dataclass
class Task():
    _Element: Element = field(init=True)
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

    _lastRun:DT = field(init=False, default_factory=DT)

    EventInfo:"EventInfo" = field(init=False, default_factory=DINT)

    RateDT:DT = None
    def __post_init__(self):
        self.Name = self._Element.get("Name", None)
        self.Class = self._Element.get("Class", None)
        self.Type = self._Element.get("Type", None)

        self.Rate = DINT(self._Element.get("Rate", 0)) * 1000
        self.RateDT = DT(self.Rate.getPLCValue())

        self.Priority = DINT(self._Element.get("Priority", 0))
        self.Watchdog = DINT(self._Element.get("Watchdog", 0)) * 1000

        if BOOL(self._Element.get("DisableUpdateOutputs", False)):
            self.DisableUpdateOutputs.setValue(1)
        else:
            self.DisableUpdateOutputs.setValue(0)

        if BOOL(self._Element.get("InhibitTask", False)):
            self.InhibitTask.setValue(1)
        else:
            self.InhibitTask.setValue(0)

        for program in self._Element.findall("./ScheduledPrograms//ScheduledProgram"):
            self._programs.append(program.get("Name", None))

        self.EventInfo = EventInfo(self._Element.find("./EventInfo"))

    @asynccontextmanager
    async def task_context(self):
        token = CurrentTaskName.set(self.Name)
        try:
            yield
        finally:
            CurrentTaskName.reset(token)

    @asynccontextmanager
    async def task_time(self):
        start = getTimeMonotonic()
        try:
            yield
        finally:
            end = getTimeMonotonic()
            diff = end - start
            
            self.LastScanTime.setValue(diff)
            if self.MaxScanTime < diff:
                self.MaxScanTime.setValue(diff)

    async def execute(self, programs:Dict[str, Program], instruction:bool = False):
        if self.InhibitTask == 0:
            self.StartTime = DT()

            run = False
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

                async with self.task_context(), self.task_time():
                    for program in self._programs:
                        await programs[program].execute()
