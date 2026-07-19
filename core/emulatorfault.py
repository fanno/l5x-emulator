from collections import deque

from engine.errors import MajorException, MinorException

class EmulatorFault:
    MajorFault:MajorException = None
    MinorFault = deque(maxlen=100)

    @staticmethod
    def prepend(fault:MinorException) -> None:
        EmulatorFault.MinorFault.appendleft(fault)

    @staticmethod
    def getMinorFault() -> list[MinorException]:
        return list(EmulatorFault.MinorFault)

    @staticmethod
    def getMajorFault() -> None|MajorException:
        return EmulatorFault.MajorFault
    
    @staticmethod
    def setMajorFault(MajorFault:MajorException) -> None:
        if EmulatorFault.MajorFault is None:
            EmulatorFault.MajorFault = MajorFault

    @staticmethod
    def hasMajorFault() -> bool:
        return EmulatorFault.MajorFault is not None