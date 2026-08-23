from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from engine.sfc.step import Step
from engine.sfc.stop import Stop
from engine.sfc.transition import Transition
from engine.sfc.directedlink import DirectedLink
from engine.sfc.branch import Branch
import engine.context

@dataclass
class SFC:
    element: InitVar[Element]

    steps:dict[int, Step] = field(init=False, default_factory=dict)
    stops:dict[int, Stop] = field(init=False, default_factory=dict)
    transitions:dict[int, Transition] = field(init=False, default_factory=dict)
    links:dict[int, DirectedLink] = field(init=False, default_factory=dict)
    branches:dict[int, Branch] = field(init=False, default_factory=dict)

    StepName: str = field(init=False, default=None)
    TransitionName: str = field(init=False, default=None)
    ActionName: str = field(init=False, default=None)
    StopName: str = field(init=False, default=None)

    active_steps:set[int] = field(init=False, default_factory=set)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.StepName = element.get('StepName')
            self.TransitionName = element.get('TransitionName')
            self.ActionName = element.get('ActionName')
            self.StopName = element.get('StopName')

            # Steps
            for step in element.findall('./Step'):
                s = Step(step)
                self.steps[s.ID] = s

            for stop in element.findall('./Stop'):
                st = Stop(stop)
                self.stops[st.ID] = st

            for transition in element.findall('./Transition'):
                t = Transition(transition)
                self.transitions[t.ID] = t

            for link in element.findall('./DirectedLink'):
                l = DirectedLink(link)
                self.links[l.FromID] = l
            for branch in element.findall('./Branch'):
                b = Branch(branch)
                self.branches[b.ID] = b

            for idx, step in self.steps.items():
                step.addConections(self)

            for idx, transition in self.transitions.items():
                transition.addConections(self)

            self.active_steps = set()
            for idx, step in self.steps.items():
                if isinstance(step, Step):
                    if step.InitialStep:
                        self.active_steps.add(idx)
                        break

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        emulator = engine.context.EmulatorContext.get()

        if emulator.preScan:
            for idx, stop in self.stops.items():
                await stop.preScan(ctx)

            for idx, step in self.steps.items():
                await step.preScan(ctx)
        else:
            to_remove = set()
            to_add = set()

            for idx, stop in self.stops.items():
                if idx not in self.active_steps:
                    await stop.notExecute(ctx)

            for idx, stop in self.stops.items():
                if idx in self.active_steps:
                    await stop.execute(ctx)

            if ctx.SFC.Paused == 0:
                for idx, step in self.steps.items():
                    if idx not in self.active_steps:
                        await step.notExecute(ctx)

                for step_id in sorted(self.active_steps):
                    step = self.steps[step_id]
                    await step.execute(ctx)
                    new_steps = await step.try_advance(ctx)

                    if new_steps:
                        to_remove.add(step_id)
                        to_add.update(new_steps)
            else:
                for step_id in sorted(self.active_steps):
                    step = self.steps[step_id]
                    await step.paused(ctx)

            self.active_steps -= to_remove
            self.active_steps |= to_add