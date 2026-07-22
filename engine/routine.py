import logging

from xml.etree.ElementTree import Element

from typing import Optional, List

from dataclasses import dataclass, field

from enum import Enum

import engine.context
from engine.rung import Rung
from engine.st.parser import normalizeST, createPython

from datatypes.custom.numbers import INT

from datatypes.sfc import SFC_STEP

class RoutineType(Enum):
    RLL = 1
    ST = 2
    FBD = 3
    SFC = 4
'''
def make_async_st(st_source: str) -> str:
    indented = indent(st_source, "    ")
    if not indented.strip():
        indented = "    pass"
    return "async def __st_main__():\n" + indented + "\n"

def indent(code: str, prefix: str) -> str:
    return "\n".join(
        prefix + line if line.strip() else line
        for line in code.splitlines()
    )
'''

@dataclass
class Routine:
    _Element: Element = field(init=True)
    Rungs: List["Rung"] = field(init=False, default_factory=lambda: [])
    ST:str = field(init=False, default=None)
    Name: Optional[str] = field(init=False, default=None)
    Type: Optional[RoutineType] = field(init=False, default=None)

    SFCPaused: INT = field(init=False, default_factory=INT)
    SFCResuming: INT = field(init=False, default_factory=INT)
    SFCStep: SFC_STEP = field(init=False, default_factory=SFC_STEP)

    def __post_init__(self):
        self.Name = self._Element.get("Name", None)
        self.Type = RoutineType[self._Element.get("Type", None)]
        
        if self.Type == RoutineType.RLL:
            for rung in self._Element.findall("./RLLContent//Rung"):
                text = rung.find("Text", None)
                if text is not None:
                    self.Rungs.append(Rung(Text=text.text))
        elif self.Type == RoutineType.ST:
            from engine.st.hooks import make_async_st
            lines = []

            try:
                for line in self._Element.findall("./STContent//Line"):
                    lines.append(line.text.strip())

                r1 = normalizeST(lines)
                self.ST = createPython(r1)
                self.ST = make_async_st(self.ST)
                
            except Exception as e:
                raise AssertionError(f"Parsing Error: {self.Name}").with_traceback(e.__traceback__)

    async def execute(self, ctx:"engine.context.ExecutionContext"):
        ctx.RoutineRef = self
        ctx.Type = self.Type
        match self.Type:
            case RoutineType.RLL:
                runRoutine = True
                while runRoutine:
                    runRoutine = False
                    for rung in self.Rungs:
                        if ctx.Jump is None or ctx.Jump == rung.getLabel():
                            ctx.Jump = None
                            ctx.RungEnabled = True
                            await rung.execute(ctx)

                            if ctx.EOT or ctx.TND:
                                break
                            elif ctx.Jump is not None:
                                runRoutine = True
                                break
            case RoutineType.ST:
                from engine.st.hooks import run_exec_env

                await run_exec_env(self.ST, ctx, self.Name, False)
            case RoutineType.FBD:
                # TODO
                pass
            case RoutineType.SFC:
                if self.SFCPaused == 0:
                    # TODO
                    pass