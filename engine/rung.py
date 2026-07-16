from typing import Optional

from dataclasses import dataclass, field

import engine.context
from engine.node import parse, InstructionNode
    
@dataclass
class Rung:
    Text:str = field(init=True)
    Tree:Optional[InstructionNode] = field(init=False, default=None)
    Label: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        self.Text = self.Text.replace(" ", "")
        self.Text = self.Text.strip().rstrip(";").strip()

        self.Tree = parse(self.Text)

    def getLabel(self) -> None | str:
        return self.Tree.getLabel()

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        if ctx.inMCR:
            ctx.RungStatus = ctx.MCRActive
        else:
            ctx.RungStatus = True
        await self.Tree.eval(ctx)