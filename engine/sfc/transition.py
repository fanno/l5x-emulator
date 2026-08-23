from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from datatypes.custom.bool import BOOL

from core.memory.helper import getMemory

import engine.context
import engine.sfc.sfc
import engine.sfc.step

@dataclass
class Transition:
    element: InitVar[Element]

    ID: int = field(init=False, default=None)
    X: str = field(init=False, default=None)
    Y: str = field(init=False, default=None)
    Operand: str = field(init=False, default=None)
    Value:BOOL = field(init=False, default=None)

    outgoing: list["engine.sfc.step.Step"] = field(default_factory=list)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.ID = int(element.get('ID'))
            self.X = int(element.get('X'))
            self.Y = int(element.get('Y'))
            self.Operand = element.get('Operand')

            from engine.st.st import ST
            content = element.find('./Condition/STContent')
            st = ST(content)
            self.ST = st.getPython(isReturn=True)

    async def preScan(self, ctx:"engine.context.ExecutionContext") -> None:
        self.Value = getMemory(self.Operand)
            
    async def execute(self, ctx:"engine.context.ExecutionContext") -> list["engine.sfc.step.Step"]:
        from engine.st.hooks import run_exec_env

        evaluated = await run_exec_env(self.ST, ctx, f"Transition: {self.ID}")

        result = []
        if evaluated:
            for step in self.outgoing:
                result.append(step)
            self.Value.setValue(True)
        else:
            self.Value.setValue(False)
        return result

    def addConections(self, sfc:"engine.sfc.sfc.SFC"):
        for link in sfc.links.values():
            if self.ID == link.FromID:
                if link.ToID in sfc.steps:
                    step = sfc.steps[link.ToID]
                    self.outgoing.append(step)
                elif link.ToID in sfc.branches:
                    branch = sfc.branches[link.ToID]
                    for legs in branch.legs:
                        step = sfc.steps[sfc.links[legs].ToID]
                        self.outgoing.append(step)