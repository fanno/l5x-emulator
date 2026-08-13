import time
import logging
from contextlib import contextmanager

from core.errors import TNDException

class EngineException(Exception):
    time:float
    hierarchy:str = ''

    def __init__(self, message):
        super().__init__(message)
        self.time = time.monotonic()

        from engine.hierarchy import Hierarchy
        self.hierarchy = Hierarchy.path()

class STException(EngineException):
    line_no:int = None
    line_text:str = None
    st:str = None

    def __init__(self, name: str, st: str, e: Exception):
        self.name = name
        self.st = st
        self.original_exception = e

        self.line_no = None
        self.line_text = None

        if isinstance(e, SyntaxError):
            self.line_no = e.lineno
            self.line_text = e.text.strip() if e.text else None
        else:
            tb = e.__traceback__
            while tb and tb.tb_next:
                tb = tb.tb_next

            if tb:
                self.line_no = tb.tb_lineno

        if self.line_no:
                lines = st.splitlines()
                if 1 <= self.line_no <= len(lines):
                    self.line_text = lines[self.line_no - 1].rstrip()

        msg = f"ST Error in: {name}"

        if self.line_no is not None:
            msg += f", line {self.line_no}"

        if self.line_text:
            msg += f"\nCode: {self.line_text}"

        from engine.hierarchy import Hierarchy
        msg += f"\nPath: {Hierarchy.path()}"

        msg += f"\n{type(e).__name__}: {e}"

        super().__init__(msg)

class PLCFault(EngineException):
    type:int
    code:int

    def __init__(self, message, _type:int=0, code:int=0):
        super().__init__(message)
        self.type = _type
        self.code = code

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
            logging.warning(f"MinorFault: {e.hierarchy}", exc_info=e)

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
            logging.error(f"MajorFault: {e.hierarchy}", exc_info=e)

    @classmethod
    @contextmanager
    def st(cls, error_tag, expression):
        try:
            yield
        except TNDException as e:
            return
        except SyntaxError as e:
            ste = STException(error_tag, expression, e)
            logging.error(f"STException:", exc_info=ste)
            #raise ste from e
        
