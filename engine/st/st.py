class ST:
    _indent:int = 0
    out:list[str] = []
    block_stack:list[str] = []

    INDENT_SIZE:int = 4

    def __init__(self):
        self.out = []
        self.block_stack = []

    def addIndent(self, amount:int=1) -> None:
        self._indent += (self.INDENT_SIZE * amount)

    def removeIndent(self, amount:int=1) -> None:
        self._indent -= (self.INDENT_SIZE * amount)

    def getIndent(self) -> str:
        return " " * self._indent