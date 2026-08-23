from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from datatypes.sfc import SFC_STOP

from core.memory.helper import getMemory

import engine.context

@dataclass
class Stop:
    element: InitVar[Element]

    ID:int = field(init=False, default=-1)
    X:str = field(init=False, default=-1)
    Y:str = field(init=False, default=-1)
    Operand: str = field(init=False, default=None)
    Value:SFC_STOP = field(init=False, default=None)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.ID = int(element.get('ID', '-1'))
            self.X = int(element.get('X', '-1'))
            self.Y = int(element.get('Y', '-1'))
            self.Operand = element.get('Operand')

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        ctx.SFC.Paused.setValue(1)

        self.Value.X.setValue(True)

    async def notExecute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value.X.setValue(False)