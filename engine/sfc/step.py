from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

from core.memory.helper import getMemory

import engine.context

from engine.sfc.action import Action

@dataclass
class Step:
    _Element: Element = field(init=True, default=None)

    ID: int = field(init=False, default=None)
    X: str = field(init=False, default=None)
    Y: str = field(init=False, default=None)
    Operand: str = field(init=False, default=None)
    Value:DataVariant|Array|UDT = field(init=False, default=None)
    InitialStep: bool = field(init=False, default=False)
    PresetUsesExpr: bool = field(init=False, default=False)
    LimitHighUsesExpr: bool = field(init=False, default=False)
    LimitLowUsesExpr: bool = field(init=False, default=False)
    ShowActions: bool = field(init=False, default=False)

    actions:list[Action] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self._Element:
            self.ID = int(self._Element.get('ID'))
            self.X = int(self._Element.get('X'))
            self.Y = int(self._Element.get('Y'))
            self.Operand = self._Element.get('Operand')
            self.InitialStep = bool(self._Element.get('InitialStep'))
            self.PresetUsesExpr = bool(self._Element.get('PresetUsesExpr'))
            self.LimitHighUsesExpr = bool(self._Element.get('LimitHighUsesExpr'))
            self.LimitLowUsesExpr = bool(self._Element.get('LimitLowUsesExpr'))
            self.ShowActions = bool(self._Element.get('ShowActions'))

            # Steps
            for action in self._Element.findall('.//Action'):
                self.actions.append(Action(action))
            
    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

        for action in self.actions:
            action.execute(ctx)