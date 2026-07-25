import time
import logging
from contextlib import contextmanager

class EngineException(Exception):
    time:float

    def __init__(self, message):
        super().__init__(message)
        self.time = time.monotonic()

class AOIException(EngineException):
    def __init__(self, name:str, instance:str):
        super().__init__(f"AOI: Name {name}, Instance {instance}")
        self.name = name
        self.instance = instance

class STException(EngineException):
    original_exception:Exception
    
    def __init__(self, name:str, st:str, e:Exception):
        super().__init__(f"ST Error in: {name}, {st}")
        self.name = name
        self.st = st
        self.original_exception = e

class PLCFault(EngineException):
    type:int
    code:int
    path:str = ''

    def __init__(self, message, _type:int=0, code:int=0):
        super().__init__(message)
        self.type = _type
        self.code = code
        from engine.hierarchy import Hierarchy
        self.path = Hierarchy.path()

class MajorFault(PLCFault):
    def __init__(self, _type:int=0, code:int=0):
        super().__init__(f"Major Fault, Type {_type}, Code {code}", _type, code)

class MinorFault(PLCFault):
    def __init__(self, _type:int=0, code:int=0):
        super().__init__(f"Minor Fault, Type {_type}, Code {code}", _type, code)

class PLCFaultHandler:
    @classmethod
    @contextmanager
    def minor(cls):
        try:
            yield
        except MinorFault as e:
            from eventbus.eventbus import EventBus
            from core.events import MinorFaultEvent

            EventBus.get().dispatch(
                MinorFaultEvent(
                    fault=e
                )
            )
            logging.warning(f"MinorFault: {e.path}", exc_info=e)

    @classmethod
    @contextmanager
    def major(cls):
        try:
            yield
        except MajorFault as e:
            from eventbus.eventbus import EventBus
            from core.events import MajorFaultEvent

            EventBus.get().dispatch(
                MajorFaultEvent(
                    fault=e
                )
            )
            logging.error(f"MajorFault: {e.path}", exc_info=e)

    @classmethod
    @contextmanager
    def st(cls):
        try:
            yield
        except STException as e:
            from core.events import STException

            logging.error(f"STException: {e.name} > {e.st}", exc_info=e)