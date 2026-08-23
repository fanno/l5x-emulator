from lxml.etree import _Element as Element

from typing import Optional, Dict, List

from dataclasses import dataclass, field, InitVar

import engine.instruction
import engine.context
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler
from engine.fbd.wire import Wire

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

from core.memory.helper import getMemory, setMemory

@dataclass
class FBDBlock:
    type: InitVar[str]
    element: InitVar[Element]

    ID:int = field(init=False, default=None)
    X:int = field(init=False, default=None)
    Y:int = field(init=False, default=None)
    Type:str = field(init=False, default=None)

    Function:Optional[str] = field(init=False, default=None)
    Operand:Optional[str] = field(init=False, default=None)
    Value:Optional[DataVariant|Array|UDT] = field(init=False, default=None)
    Signal: Optional[str] = field(init=False, default=None)
    instance:"engine.instruction.Instruction" = None

    incoming_wires: List[Wire] = field(init=False, default_factory=list)
    outgoing_wires: List[Wire] = field(init=False, default_factory=list)
    inParams: Dict[str, Wire] = field(init=False, default_factory=dict)
    outParams: Dict[str, Wire] = field(init=False, default_factory=dict)

    def __post_init__(self, type:str, element:Element):
        if isinstance(element, Element):
            self.Type = type

            self.ID = int(element.get('ID', '-1'))
            self.X = int(element.get('X', '0'))
            self.Y = int(element.get('Y', '0'))
            self.Function = element.get('Type', None)
            self.Operand = element.get('Operand', None)

            if self.Type in ('ICon', 'OCon'):
                self.Signal = element.get('Name', None)

        from core.registry.instructionregistry import InstructionRegistry

        if self.Function:
            cls = InstructionRegistry.get(self.Function)
            self.instance = cls(self.Function)
        else: 
            self.instance = None

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        with Hierarchy.scope(f"Block[{self.Type}, {str(self.Function)}]"):
            with PLCFaultHandler.minor():
                if self.Operand and self.Value is None:
                    self.Value = getMemory(self.Operand)

                if self.Type == 'ICon':
                    if self.Signal:
                        if self.Signal in ctx.RoutineRef.Signals:
                            self.Value = ctx.RoutineRef.Signals[self.Signal]
                            if self.Value is not None:
                                for wire in self.outgoing_wires:
                                    wire.Value = self.Value
                elif self.Type == 'OCon':
                    if self.Signal:
                        for wire in self.incoming_wires:
                            ctx.RoutineRef.Signals[self.Signal] = wire.Value
                            break
                elif self.Type == 'IRef':
                    for wire in self.outgoing_wires:
                        wire.Value = self.Value
                elif self.Type == 'Function' or self.Type == 'Block':
                    await self.instance.fbd(ctx, self)
                elif self.Type == 'ORef':
                    for wire in self.incoming_wires:
                        if wire.Value is not None:
                            setMemory(self.Operand, wire.Value)

    def bindWire(self, wires:list[Wire]):
        for idx, wire in enumerate(wires):
            if self.ID == wire.FromID:
                self.outgoing_wires.append(wire)
                if wire.FromParam:
                    self.outParams[wire.FromParam]  = wire

            if self.ID == wire.ToID:
                self.incoming_wires.append(wire)
                if wire.ToParam:
                    self.inParams[wire.ToParam]  = wire