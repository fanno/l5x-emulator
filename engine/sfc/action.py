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
    RaiseEdge:bool = field(init=False, default=False)
    FallEdge:bool = field(init=False, default=False)
    keepRunning:bool = field(init=False, default=False)
    count:bool = field(init=False, default=False)

    lastState:int = field(init=False, default=0)
    StoredTimeDelayed:bool = field(init=False, default=False)

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
            self.ST = st.getPython(self.IsBoolean)

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)

        self.Value.Q.setValue(False)
        self.RaiseEdge = True
        self.keepRunning = False

    async def paused(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.Value.PauseTimer:
            now = ctx.Time.now_ms()
            self.last.setValue(now)

    async def notExecute(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.Qualifier == "Reset":
            return

        now = ctx.Time.now_ms()

        await self.preset(ctx)

        if self.lastState != 1:
            self.lastState = 1
            if not self.keepRunning:
                self.count = True

        self.Value.A.setValue(False)
        match self.Qualifier:
            case "NonStored": #N
                self.Value.Q.setValue(False)
            case "PulseRisingEdge": #P1
                self.Value.Q.setValue(False)
            case "TimeLimited": #L
                self.Value.Q.setValue(False)
            case "Stored": #S
                if self.keepRunning:
                    await self.run(ctx)
            case "StoredTimeLimited": #SL
                if self.keepRunning:
                    self.updateTimer(now)

                    if self.Value.PRE > self.Value.T:
                        await self.run(ctx)
                    else:
                        self.keepRunning = False
            case "TimeDelayed": #D
                if self.keepRunning:
                    await self.run(ctx)
            case "TimeDelayedStored": #DS
                raise NotImplementedError(f"FCS Action, {Action}, Qualifier, {self.Qualifier} not implemented yet")
            case "StoredTimeDelayed": #SD
                if self.keepRunning:
                    self.updateTimer(now)

                    if self.Value.PRE <= self.Value.T:
                        await self.run(ctx)
            case "Pulse": #P
                if self.FallEdge:
                    await self.run(ctx)
                    self.FallEdge = False
            case "PulseFallingEdge": #PO
                if  self.FallEdge:
                    await self.run(ctx)
                    self.FallEdge = False
            case _:
                raise NotImplementedError(f"FCS Action, {Action}, Qualifier, {self.Qualifier} not implemented yet")

        self.RaiseEdge = True
        self.FallEdge = False
        self.last.setValue(now)

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.Qualifier == "Reset":
            for idx, step in ctx.RoutineRef._SFC.steps.items():
                for action in step.actions:
                    if action.Operand == self.Operand:
                        await action.reset(ctx)
            return

        if self.lastState != 2:
            self.lastState = 2
            self.count = True

        await self.preset(ctx)

        self.FallEdge = True

        now = ctx.Time.now_ms()
        if self.RaiseEdge:
            self.last.setValue(now)
            self.Value.T.setValue(0)

        self.Value.A.setValue(False)
        match self.Qualifier:
            case "NonStored": #N
                self.updateTimer(now)

                await self.run(ctx)
            case "PulseRisingEdge": #P1
                if self.RaiseEdge:
                    await self.run(ctx)
            case "TimeLimited": #L
                self.updateTimer(now)

                if self.Value.PRE > self.Value.T:
                    await self.run(ctx)
            case "Stored": #S
                self.keepRunning = True
                await self.run(ctx)
            case "StoredTimeLimited": #SL
                self.updateTimer(now)

                if self.Value.PRE >= self.Value.T:
                    self.keepRunning = True
                    await self.run(ctx)
                else:
                    self.keepRunning = False
            case "TimeDelayed": #D
                self.updateTimer(now)
                
                if self.Value.PRE <= self.Value.T:
                    self.keepRunning = True
                    await self.run(ctx)
            case "TimeDelayedStored": #DS
                raise NotImplementedError(f"FCS Action, {Action}, Qualifier, {self.Qualifier} not implemented yet")
            case "StoredTimeDelayed": #SD
                self.updateTimer(now)

                self.keepRunning = True
                if self.Value.PRE <= self.Value.T:
                    await self.run(ctx)
            case "Pulse": #P
                if self.RaiseEdge:
                    await self.run(ctx)
                    self.Value.Count.setValue(self.Value.Count + 1)
            case "PulseFallingEdge": #PO
                self.FallEdge = True
            case _:
                raise NotImplementedError(f"FCS Action, {Action}, Qualifier, {self.Qualifier} not implemented yet")

        self.RaiseEdge = False
        self.FallEdge = True
        self.last.setValue(now)

    async def run(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value.A.setValue(True)
        result = await run_exec_env(self.ST, ctx, f"Action->{self.Qualifier}: {self.ID}", False)
        if self.IsBoolean:
            self.Value.Q.setValue(result)

        if self.count:
            self.Value.Count.setValue(self.Value.Count + 1)
            self.count = False

    async def preset(self, ctx:"engine.context.ExecutionContext") -> None:
        if self.PresetUsesExpr:
            value = await run_exec_env(self.PresetExpr, ctx, f"Action->preset->PresetExpr: {self.ID}", False)
            self.Value.PRE.setValue(value)

    async def reset(self, ctx:"engine.context.ExecutionContext") -> None:
        self.keepRunning = False

    def updateTimer(self, now:DINT) -> None:
        if self.Value.PRE > self.Value.T:
            if self.last > 0:
                self.Value.T.setValue(self.Value.T + (now - self.last))

        self.last.setValue(now)