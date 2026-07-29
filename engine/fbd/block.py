from xml.etree.ElementTree import Element

from typing import Optional, Dict, List

from dataclasses import dataclass, field

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
    _Type:str = field(init=True)
    _Element:Element = field(init=True)

    ID:int = field(init=False, default=None)
    X:int = field(init=False, default=None)
    Y:int = field(init=False, default=None)

    Function:Optional[str] = field(init=False, default=None)
    Operand:Optional[str] = field(init=False, default=None)
    Value:Optional[DataVariant|Array|UDT] = field(init=False, default=None)
    Signal: Optional[str] = field(init=False, default=None)
    instance:"engine.instruction.Instruction" = None

    incoming_wires: List[Wire] = field(init=False, default_factory=list)
    outgoing_wires: List[Wire] = field(init=False, default_factory=list)
    inParams: Dict[str, Wire] = field(init=False, default_factory=dict)
    outParams: Dict[str, Wire] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.ID = int(self._Element.get('ID', '-1'))
        self.X = int(self._Element.get('X', '0'))
        self.Y = int(self._Element.get('Y', '0'))
        self.Function = self._Element.get('Type', None)
        self.Operand = self._Element.get('Operand', None)

        if self._Type in ('ICon', 'OCon'):
            self.Signal = self._Element.get('Name', None)

        from core.registry.instructionregistry import InstructionRegistry

        if self.Function:
            cls = InstructionRegistry.get(self.Function)
            self.instance = cls(self.Function)
        else: 
            self.instance = None

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        with Hierarchy.scope(f"Block[{self._Type}{str(self.Function)}]"):
            with PLCFaultHandler.minor():
                if self.Operand and self.Value is None:
                    self.Value = getMemory(self.Operand)

                if self._Type == 'ICon':
                    if self.Signal:
                        if self.Signal in ctx.RoutineRef.Signals:
                            self.Value = ctx.RoutineRef.Signals[self.Signal]
                            if self.Value is not None:
                                for wire in self.outgoing_wires:
                                    wire.Value = self.Value
                elif self._Type == 'OCon':
                    if self.Signal:
                        for wire in self.incoming_wires:
                            ctx.RoutineRef.Signals[self.Signal] = wire.Value
                            break
                elif self._Type == 'IRef':
                    for wire in self.outgoing_wires:
                        wire.Value = self.Value
                elif self._Type == 'Function' or self._Type == 'Block':
                    await self.instance.fbd(ctx, self)
                elif self._Type == 'ORef':
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