from xml.etree.ElementTree import Element

from asyncua import Server

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.program import Program

async def loadPrograms(controller:Element, server:Server, programs:Dict[str, "Program"]):
    #for program in controller.findall("./Programs//Program[@Class='Standard']"):
    from engine.program import Program

    for program in controller.findall("./Programs//Program"):
        p = Program(_Element=program,
                    server=server,
                    Name=program.get("Name"))
        await p.init()
        programs[p.Name] = p