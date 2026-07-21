class EmulatorContext():
    preScan:bool
    postScan:bool

    def __init__(self, pre:bool=False, post:bool=False):
        self.preScan = pre
        self.postScan = post