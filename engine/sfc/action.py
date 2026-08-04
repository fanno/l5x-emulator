from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from datatypes.sfc import SFC_ACTION
from datatypes.custom.numbers import DINT

from core.memory.helper import getMemory

from engine.st.st import ST
import engine.context

from engine.st.hooks import run_exec_env

@dataclass
class Action:
    _Element: Element = field(init=True, default=None)

    ID: int = field(init=False, default=None)
    Operand: str = field(init=False, default=None)
    Value:SFC_ACTION = field(init=False, default=None)
    PresetUsesExpr: bool = field(init=False, default=False)
    IsBoolean: bool = field(init=False, default=False)
    Qualifier: str = field(init=False, default=None)

    PresetExpr: str = field(init=False, default=None)

    last:DINT = field(init=False, default_factory=DINT)

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.ID = int(self._Element.get('ID'))
            self.Operand = self._Element.get('Operand')
            self.Qualifier = self._Element.get('Qualifier')
            self.PresetUsesExpr = bool(self._Element.get('PresetUsesExpr'))
            self.IsBoolean = bool(self._Element.get('IsBoolean'))

            if self.PresetUsesExpr:
                st = ST(self._Element.find('./Preset/STContent'))
                self.PresetExpr = st.getPython(True)

            content = self._Element.find('./Body/STContent')
            st = ST(content)
            self.ST = st.getPython()

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

        self.Value.Q.setValue(False)

    async def paused(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.Value.PauseTimer:
            now = ctx.Time.now_ms()
            self.last.setValue(now)

    async def notExecute(self, ctx:"engine.context.ExecutionContext") -> None:
        self.last.setValue(0)
        self.Value.A.setValue(False)
        self.Value.Q.setValue(False)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.PresetUsesExpr:
            value = await run_exec_env(self.PresetExpr, ctx, f"PresetExpr: {self.ID}", False)
            self.Value.PRE.setValue(value)

        match self.Qualifier:
            case "NonStored":
                await run_exec_env(self.ST, ctx, f"Action: {self.ID}", False)

                now = ctx.Time.now_ms()
                if  self.last > 0:
                    self.Value.T.setValue(self.Value.T + (now - self.last))
                else:
                    self.Value.Count.setValue(self.Value.Count + 1)

                self.last.setValue(now)

                self.Value.A.setValue(True)
            case _:
                raise NotImplementedError(f"FCS Action, {Action}, Qualifier, {self.Qualifier} not implemented yet")