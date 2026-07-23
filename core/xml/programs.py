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
                    Name=program.get("Name"),
                    Type=program.get("Type"),
                    TestEdits=program.get("TestEdits"),
                    PreStateRoutineName=program.get("PreStateRoutineName"),
                    FaultRoutineName=program.get("FaultRoutineName"),
                    InitialStepIndex=program.get("InitialStepIndex"),
                    InitialState=program.get("InitialState"),
                    CompleteStateIfNotImpl=program.get("CompleteStateIfNotImpl"),
                    LossOfCommCmd=program.get("LossOfCommCmd"),
                    ExternalRequestAction=program.get("ExternalRequestAction"),
                    UseAsFolder=program.get("ExterUseAsFoldernalRequestAction"),
                    AutoValueAssignStepToPhase=program.get("AutoValueAssignStepToPhase"),
                    AutoValueAssignPhaseToStepOnComplete=program.get("AutoValueAssignPhaseToStepOnComplete"),
                    AutoValueAssignPhaseToStepOnStopped=program.get("AutoValueAssignPhaseToStepOnStopped"),
                    AutoValueAssignPhaseToStepOnAborted=program.get("AutoValueAssignPhaseToStepOnAborted"))
        
        await p.init()
        programs[p.Name] = p