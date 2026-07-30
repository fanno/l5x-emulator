from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from engine.sfc.step import Step
import engine.context

@dataclass
class SFC:
    _Element: Element = field(init=True, default=None)

    steps:list[int, Step] = field(init=False, default_factory=list)

    StepName: str = field(init=False, default=None)
    TransitionName: str = field(init=False, default=None)
    ActionName: str = field(init=False, default=None)
    StopName: str = field(init=False, default=None)

    def __post_init__(self):
        if self._Element:
            self.StepName = self._Element.get('StepName')
            self.TransitionName = self._Element.get('TransitionName')
            self.ActionName = self._Element.get('ActionName')
            self.StopName = self._Element.get('StopName')

            # Steps
            for step in self._Element.findall('.//Step'):
                self.steps.append(Step(step))

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        for self in self.steps:
            self.execute(ctx)