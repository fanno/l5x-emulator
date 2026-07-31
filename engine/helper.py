import contextvars

from typing import List

from engine.aoi.memory import AOIMemory

CurrentTaskName = contextvars.ContextVar('CurrentTaskName', default=None)
CurrentProgramName = contextvars.ContextVar('CurrentProgramName', default=None)
CurrentAOI: contextvars.ContextVar[List[AOIMemory]] = contextvars.ContextVar('CurrentAOI', default=[])