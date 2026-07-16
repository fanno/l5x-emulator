import time

from datatypes.custom.numbers import DINT

class TimeBase:
    @staticmethod
    def now() -> DINT:
        return DINT(getTimeMonotonic(1000))
    
def getTimeMonotonic(factor:int=1000000) -> int:
    return int(time.monotonic() * factor)