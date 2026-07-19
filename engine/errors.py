import time

class EngineException(Exception):
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

class MajorException(EngineException):
    def __init__(self, _type:int, code:int):
        super().__init__(f"Major Fault, Type {_type}, Code {code}")
        self.type = _type
        self.code = code

class MinorException(EngineException):
    def __init__(self, _type:int, code:int):
        super().__init__(f"Minor Fault, Type {_type}, Code {code}")
        self.type = _type
        self.code = code
