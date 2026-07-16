from dataclasses import dataclass, field

@dataclass
class Logger:
    max_size: int = field(init=False, default=1000)
    _logs:list[str] = field(init=False, repr=False, default_factory=list)
    _changed:bool = field(init=False, repr=False, default=False)

    def addEntry(self, entry:str):
        self._logs.append(entry)
        self._changed = True
        if self.getSize() > self.max_size:
            self._logs.pop(0)

    def hasChanged(self) -> bool:
        changed = self._changed
        self._changed = False
        return changed
    
    def getLogs(self) -> list[str]:
        return self._logs
    
    def getSize(self) -> int:
        return len(self._logs)