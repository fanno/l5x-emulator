from lxml.etree import _Element as Element

from asyncua import Server

from typing import Dict, TYPE_CHECKING, Set

if TYPE_CHECKING:
    from engine.program import Program

from opcua.updater import OPCUAUpdater

from core.events import LoadingEvent
from eventbus.eventbus import EventBus

async def loadPrograms(controller:Element, server:Server, programs:Dict[str, "Program"]):
    #for program in controller.findall("./Programs//Program[@Class='Standard']"):
    from engine.program import Program

    for program in controller.findall("./Programs//Program"):
        EventBus.get().dispatch(LoadingEvent(f"Program: {program.get("Name")}"))

        p = Program(element=program,
                    server=server)
        
        await p.init()
        programs[p.Name] = p