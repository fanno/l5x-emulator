import logging

import time

from contextlib import asynccontextmanager

from xml.etree.ElementTree import Element

from typing import Optional, Dict, TYPE_CHECKING

from dataclasses import dataclass, field

from asyncua import Server, ua

if TYPE_CHECKING:
    from core.memory.memory import Memory
    
from engine.routine import Routine

from core.xml.tags import loadTags
from core.timebase import getTimeMonotonic

from opcua.tag import OpcuaTag
from opcua.mapping import Mapping

from datatypes.custom.numbers import SINT, DINT
from datatypes.custom.array import Array

from engine.errors import STException
from engine.errors import MajorFault

@dataclass
class Program():
    _Element: Element = field(init=True)
    Name:str = field(init=True)
    server:Server = field(init=True)

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

    async def execute(self):
        if self.MainRoutineName in self.Routines:
            if self.DisableFlag == 0:
                async with self.program_context(), self.program_time():
                    from engine.context import ExecutionContext
                    context = ExecutionContext(ProgramRef=self)
                    await self.Routines[self.MainRoutineName].execute(context)
            else:
                self.LASTSCANTIME.setValue(0)
                self.MAXSCANTIME.setValue(0)