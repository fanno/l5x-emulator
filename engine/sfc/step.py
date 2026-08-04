from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from datatypes.sfc import SFC_STEP
from datatypes.custom.numbers import DINT

from core.memory.helper import getMemory

import engine.context

from engine.sfc.action import Action
from engine.sfc.transition import Transition
import engine.sfc.sfc
from engine.st.st import ST

from engine.st.hooks import run_exec_env

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

    PresetExpr: str = field(init=False, default=None)
    LimitHighExpr: str = field(init=False, default=None)
    LimitLowExpr: str = field(init=False, default=None)

    actions:list[Action] = field(init=False, default_factory=list)
    outgoing: list[Transition] = field(default_factory=list)

    last:DINT = field(init=False, default_factory=DINT)

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

            if self.PresetUsesExpr:
                st = ST(self._Element.find('./Preset/STContent'))
                self.PresetExpr = st.getPython(True)

            if self.LimitHighUsesExpr:
                st = ST(self._Element.find('./LimitHigh/STContent'))
                self.LimitHighExpr = st.getPython(True)

            if self.LimitLowUsesExpr:
                st = ST(self._Element.find('./LimitLow/STContent'))
                self.LimitLowExpr = st.getPython(True)

        # Actions
        for action in self._Element.findall('./Action'):
                self.actions.append(Action(action))

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

        for transition in self.outgoing:
            await transition.preScan(ctx)

        for action in self.actions:
            await action.preScan(ctx)

    async def paused(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.Value.PauseTimer:
            now = ctx.Time.now_ms()
            self.last.setValue(now)

        for action in self.actions:
            await action.paused(ctx)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.PresetUsesExpr:
            value = await run_exec_env(self.PresetExpr, ctx, f"PresetExpr: {self.ID}", False)
            self.Value.PRE.setValue(value)

        if self.LimitHighUsesExpr:
            value = await run_exec_env(self.LimitHighExpr, ctx, f"LimitHighExpr: {self.ID}", False)
            self.Value.AlarmHigh.setValue(value)

        if self.LimitLowUsesExpr:
            value = await run_exec_env(self.LimitLowExpr, ctx, f"LimitLowExpr: {self.ID}", False)
            self.Value.AlarmLow.setValue(value)

        for action in self.actions:
            await action.execute(ctx)

        self.Value.FS.setValue(not self.Value.X)

        now = ctx.Time.now_ms()
        
        if self.Value.FS:
            self.Value.T.setValue(0)
        else:
            self.Value.T.setValue(self.Value.T + (now - self.last))

        if self.Value.T > self.Value.TMax:
            self.Value.TMax.setValue(self.Value.T)

        self.last.setValue(now)

        self.Value.SA.setValue(True)

        self.Value.LS.setValue(False)
        if self.Value.T >= self.Value.PRE:
            if not self.Value.DN:
                self.Value.LS.setValue(True)

        self.Value.DN.setValue(self.Value.T >= self.Value.PRE)

        self.Value.X.setValue(self.Value.FS or self.Value.SA or self.Value.LS)

    async def notExecute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value.DN.setValue(False)

        self.Value.X.setValue(False)
        self.Value.FS.setValue(False)
        self.Value.SA.setValue(False)
        self.Value.LS.setValue(False)

        for action in self.actions:
            await action.notExecute(ctx)        

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