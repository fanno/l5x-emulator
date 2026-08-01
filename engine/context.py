import logging
from typing import Optional
from contextvars import ContextVar
from dataclasses import dataclass, field

import core.emulator
from core.timebase import TimeBase

from engine.program import Program
from engine.routine import Routine, RoutineType
from engine.fbd.sheet import Sheet

from datatypes.custom.bool import BOOL
from datatypes.sfc import SFC_STEP
from datatypes.custom.numbers import INT

class EmulatorContext:
    _context: ContextVar[Optional['core.emulator.Emulator']] = ContextVar(
        'emulator', default=None
    )

    @staticmethod
    def set(emulator: 'core.emulator.Emulator') -> None:
        if EmulatorContext.is_running():
            logging.warning(
                f"An emulator is already running. "
                f"Stopping existing session before starting new one."
            )
            EmulatorContext.stop()
        
        EmulatorContext._context.set(emulator)

    @staticmethod
    def stop() -> None:
        emulator = EmulatorContext.get()
        if emulator:
            try:
                logging.info("Shutting down emulator...")
                emulator.shutdown()
            except Exception as e:
                logging.error(f"Error during emulator shutdown: {e}")

        EmulatorContext.clear()
    
    @staticmethod
    def get() -> Optional['core.emulator.Emulator']:
        return EmulatorContext._context.get()
    
    @staticmethod
    def is_running() -> bool:
        return EmulatorContext.get() is not None
    
    @staticmethod
    def clear() -> None:
        EmulatorContext._context.set(None)
        
@dataclass
class SFCContext:
    Paused: INT = field(init=False, default_factory=INT)
    Resuming: INT = field(init=False, default_factory=INT)
    Step: SFC_STEP = field(init=False, default_factory=SFC_STEP)
    Status:BOOL = field(init=True, default_factory=BOOL)
    Transition:bool = field(init=True, default=False)

@dataclass
class FBDContext:
    sheet:Sheet = field(init=True, default_factory=Sheet)

@dataclass
class RLLContext:
    EOT:bool = field(init=True, default=False)
    TND:bool = field(init=True, default=False)
    PSC:bool = field(init=True, default='')
    PSR:str = field(init=True, default='False')
    Jump:str = field(init=False, default=None)
    inMCR:bool = field(init=False, default=False)
    MCRActive:bool = field(init=False, default=False)
    RungEnabled:bool = field(init=True, default=True)
    RungStatus:bool = field(init=True, default=True)    

@dataclass
class ExecutionContext:
    ProgramRef:Program = field(init=True, default=None)
    RoutineRef:Routine = field(init=False, default=None)
    Time:TimeBase = field(init=False, default_factory=TimeBase)
    Type:RoutineType = field(init=True, default=RoutineType.RLL)
    InputArgs:list = field(init=True, default_factory=list)
    ReturnArgs:list = field(init=True, default_factory=list)
    FBD:FBDContext = field(init=True, default_factory=FBDContext)
    RLL:RLLContext = field(init=True, default_factory=RLLContext)
    SFC:SFCContext = field(init=True, default_factory=SFCContext)