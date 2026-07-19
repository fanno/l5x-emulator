from collections import deque

from engine.errors import MajorFault, MinorFault

class EmulatorFault:
    Major:MajorFault = None
    Minor = deque(maxlen=100)

    @staticmethod
    def prepend(fault:MinorFault) -> None:
        EmulatorFault.Minor.appendleft(fault)

    @staticmethod
    def getMinorFault() -> list[MinorFault]:
        return list(EmulatorFault.Minor)

    @staticmethod
    def getMajorFault() -> None|MajorFault:
        return EmulatorFault.Major
    
    @staticmethod
    def setMajorFault(MajorFault:MajorFault) -> None:
        if EmulatorFault.Major is None:
            EmulatorFault.Major = MajorFault

    @staticmethod
    def hasMajorFault() -> bool:
        return EmulatorFault.Major is not None