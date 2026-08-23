from lxml.etree import _Element as Element

from typing import Optional, List

from dataclasses import dataclass, field, InitVar

from enum import Enum

import engine.context
from engine.rll.rung import Rung
from engine.fbd.sheet import Sheet
from engine.st.st import ST
from engine.sfc.sfc import SFC
from engine.executiontimer import ExecutionTimer
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

from datatypes.sfc import SFC_STEP
from datatypes.custom.numbers import INT

class RoutineType(Enum):
    RLL = 1
    ST = 2
    FBD = 3
    SFC = 4

@dataclass
class Routine:
    element: InitVar[Element]

    Rungs: List["Rung"] = field(init=False, default_factory=lambda: [])
    Sheets: List["Sheet"] = field(init=False, default_factory=lambda: [])
    ST:str = field(init=False, default=None)
    _SFC:SFC = field(init=False, default=None)
    Name: Optional[str] = field(init=False, default=None)
    Type: Optional[RoutineType] = field(init=False, default=None)
    SFCPaused: INT = field(init=False, default_factory=INT)
    SFCResuming: INT = field(init=False, default_factory=INT)
    SFCStep: SFC_STEP = field(init=False, default_factory=SFC_STEP)

    Signals:Optional[dict[str, DataVariant|Array|UDT]] = field(init=False, default_factory=lambda: {})
    
    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.Name = element.get("Name", None)
            self.Type = RoutineType[element.get("Type", None)]
            if self.Type == RoutineType.RLL:
                for rung in element.findall("./RLLContent//Rung"):
                    text = rung.find("Text", None)
                    if text is not None:
                        line = int(rung.get("Number", "-1"))
                        self.Rungs.append(Rung(Text=text.text, Line=line))
            elif self.Type == RoutineType.ST:
                content = element.find(".//STContent")
                st = ST(content)
                #self.ST = st.getPython(doPrint=self.Name == "VisionConfigG18")
                self.ST = st.getPython()

            elif self.Type == RoutineType.FBD:
                for sheet in element.findall("./FBDContent//Sheet"):
                    self.Sheets.append(Sheet(sheet))

                for sheet in self.Sheets:
                    for idx, block in sheet.blocks.items():
                        if block.Signal:
                            self.Signals[block.Signal] = block
            elif self.Type == RoutineType.SFC:
                content = element.find(".//SFCContent")

                self._SFC = SFC(content)

    async def execute(self, ctx:"engine.context.ExecutionContext"):
        with Hierarchy.scope(self.Name):
            with PLCFaultHandler.minor():
                ctx.RoutineRef = self
                ctx.Type = self.Type

                match self.Type:
                    case RoutineType.RLL:
                        runRoutine = True

                        while runRoutine:
                            runRoutine = False
                            for rung in self.Rungs:
                                if ctx.RLL.Jump is None or ctx.RLL.Jump == rung.getLabel():
                                    ctx.RLL.Jump = None
                                    ctx.RLL.RungEnabled = True
                                    await rung.execute(ctx)

                                    if ctx.RLL.EOT or ctx.RLL.TND:
                                        break
                                    elif ctx.RLL.Jump is not None:
                                        runRoutine = True
                                        break
                    case RoutineType.ST:
                        timer = ExecutionTimer()
                        with timer:
                            from engine.st.hooks import run_exec_env
                            await run_exec_env(self.ST, ctx, self.Name)
                    case RoutineType.FBD:
                        for sheet in self.Sheets:
                            await sheet.execute(ctx)
                    case RoutineType.SFC:
                        ctx.SFC.Paused = self.SFCPaused
                        ctx.SFC.Resuming = self.SFCResuming
                        ctx.SFC.Step = self.SFCStep
                        
                        if ctx.SFC.Paused == 0:
                            await self._SFC.execute(ctx)