class EngineException(Exception):
    pass

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
