import contextvars

from typing import List, Optional

from engine.aoi.memory import AOIMemory

import core.emulator 

CurrentTaskName = contextvars.ContextVar('CurrentTaskName', default=None)
CurrentProgramName = contextvars.ContextVar('CurrentProgramName', default=None)
CurrentAOI: contextvars.ContextVar[List[AOIMemory]] = contextvars.ContextVar('CurrentAOI', default=[])

def _pushAOIMemory(aoi_obj: AOIMemory) -> contextvars.Token:
    old_stack = CurrentAOI.get()
    new_stack = old_stack + [aoi_obj]
    return CurrentAOI.set(new_stack)

def _popAOIMemory(token: contextvars.Token) -> None:
    CurrentAOI.reset(token)

def currentAOIMemory() -> Optional[AOIMemory]:
    stack = CurrentAOI.get()
    return stack[-1] if stack else None