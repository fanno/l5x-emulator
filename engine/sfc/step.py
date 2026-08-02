from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from datatypes.sfc import SFC_STEP

from core.memory.helper import getMemory

import engine.context

from engine.sfc.action import Action
from engine.sfc.branch import Branch
from engine.sfc.transition import Transition
import engine.sfc.sfc

@dataclass
class Step:
    _Element: Element = field(init=True, default=None)

    ID:int = field(init=False, default=-1)
    X:str = field(init=False, default=-1)
    Y:str = field(init=False, default=-1)
    Operand: str = field(init=False, default=None)
    Value:SFC_STEP = field(init=False, default=None)
    InitialStep: bool = field(init=False, default=False)
    PresetUsesExpr: bool = field(init=False, default=False)
    LimitHighUsesExpr: bool = field(init=False, default=False)
    LimitLowUsesExpr: bool = field(init=False, default=False)
    ShowActions: bool = field(init=False, default=False)

    actions:list[Action] = field(init=False, default_factory=list)
    outgoing: list[Transition] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.ID = int(self._Element.get('ID', '-1'))
            self.X = int(self._Element.get('X', '-1'))
            self.Y = int(self._Element.get('Y', '-1'))
            self.Operand = self._Element.get('Operand')
            self.InitialStep = bool(self._Element.get('InitialStep', 'false'))
            self.PresetUsesExpr = bool(self._Element.get('PresetUsesExpr', 'false'))
            self.LimitHighUsesExpr = bool(self._Element.get('LimitHighUsesExpr', 'false'))
            self.LimitLowUsesExpr = bool(self._Element.get('LimitLowUsesExpr', 'false'))
            self.ShowActions = bool(self._Element.get('ShowActions', 'false'))

        # Actions
        for action in self._Element.findall('./Action'):
                self.actions.append(Action(action))

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

        for transition in self.outgoing:
            await transition.preScan(ctx)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        for action in self.actions:
            await action.execute(ctx)
        #TODO TIMERS ANDN STUFFF
        self.Value.DN.setValue(True)

    async def notExecute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value.DN.setValue(False)

    def addConections(self, sfc:"engine.sfc.sfc.SFC"):
        for link in sfc.links.values():
            if self.ID == link.FromID:
                if link.ToID in sfc.transitions:
                    transition = sfc.transitions[link.ToID]
                    self.outgoing.append(transition)
                elif link.ToID in sfc.branches:
                    branch = sfc.branches[link.ToID]
                    for legs in branch.legs:
                        transition = sfc.transitions[sfc.links[legs].ToID]
                        self.outgoing.append(transition)
                break

    async def try_advance(self, ctx) -> list[int]:
        if not self.Value.DN:
            return []
        new_steps = []
        for transition in self.outgoing:
            if isinstance(transition, Transition):
                results = await transition.execute(ctx)
                for step in results:
                    new_steps.append(step.ID)

        return new_steps