from typing import Optional

from dataclasses import dataclass, field

import engine.context
from engine.node import parse, Series
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler

@dataclass
class Rung:
    Text:str = field(init=True)
    Line:int = field(init=True)
    Tree:Optional[Series] = field(init=False, default=None)
    Label: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        self.Text = self.Text.replace(" ", "")
        self.Text = self.Text.strip().rstrip(";").strip()

        self.Tree = parse(self.Text)

    def getLabel(self) -> None | str:
        return self.Tree.getLabel()

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        with Hierarchy.scope(f"Rung[{str(self.Line)}]"):
            with PLCFaultHandler.minor():
                if ctx.RLL.inMCR:
                    ctx.RLL.RungStatus = ctx.RLL.MCRActive
                else:
                    ctx.RLL.RungStatus = True
                await self.Tree.eval(ctx)