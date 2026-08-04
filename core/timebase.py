import time

from datatypes.custom.numbers import DINT, LINT

class TimeBase:
    @staticmethod
    def now_ms() -> DINT:
        return DINT(getTimeMonotonic(1000))

    @staticmethod
    def now_μs() -> LINT:
        return LINT(getTimeMonotonic())    
    
def getTimeMonotonic(factor:int=1000000) -> int:
    return int(time.monotonic() * factor)