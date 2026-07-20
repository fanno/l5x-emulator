import logging
from dataclasses import dataclass, field
from core.events import LogEvent

class IndentedFormatter(logging.Formatter):
    """Custom formatter that indents tracebacks to match log level"""
    
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        result = self.indent(result)
        return result
    
    def format(self, record):
        msg = super().format(record)
        msg = self.indent(msg)
        
        return msg
    
    def indent(self, result) -> str:
        if result:
            result = result.replace('\n', '\n    ')
        return result
    
@dataclass
class Logger:
    max_size: int = field(init=False, default=1000)
    _logs:list[LogEvent] = field(init=False, repr=False, default_factory=list)
    _changed:bool = field(init=False, repr=False, default=False)

    def addEntry(self, entry:LogEvent):
        self._logs.append(entry)
        self._changed = True
        if self.getSize() > self.max_size:
            self._logs.pop(0)

    def hasChanged(self) -> bool:
        changed = self._changed
        self._changed = False
        return changed
    
    def getLogs(self) -> list[LogEvent]:
        return self._logs
    
    def getSize(self) -> int:
        return len(self._logs)