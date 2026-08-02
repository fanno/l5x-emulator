from xml.etree.ElementTree import Element

from typing import Any, Dict, List, Set

from dataclasses import dataclass, field

import engine.context
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler
from engine.fbd.wire import Wire
from engine.fbd.block import FBDBlock

from core.memory.helper import getMemory

@dataclass
class Sheet:
    _Element: Element = field(init=True, default=None)

    Number:int = field(init=False, default=0)

    blocks:dict[int, FBDBlock] = field(init=False, default_factory=dict)
    wires:list[Wire] = field(init=False, default_factory=list)
    execution_order:list[int] = field(init=False, default_factory=list)

    def __post_init__(self):
        if isinstance(self._Element, Element):
            self.Number = int(self._Element.get('Number', '0'))

            # Blocks
            for elem in self._Element.findall('.//IRef'):
                block = FBDBlock('IRef', elem)
                self.blocks[block.ID] = block
            
            for elem in self._Element.findall('.//ORef'):
                block = FBDBlock('ORef', elem)
                self.blocks[block.ID] = block

            for elem in self._Element.findall('.//ICon'):
                block = FBDBlock('ICon', elem)
                self.blocks[block.ID] = block
            for elem in self._Element.findall('.//OCon'):
                block = FBDBlock('OCon', elem)
                self.blocks[block.ID] = block
                
            for elem in self._Element.findall('.//Function'):
                block = FBDBlock('Function', elem)
                self.blocks[block.ID] = block

            for elem in self._Element.findall('.//Block'):
                block = FBDBlock('Block', elem)
                self.blocks[block.ID] = block

            # Connections
            for elem in self._Element.findall('.//Wire'):
                self.wires.append(Wire(elem))

            for elem in self._Element.findall('.//FeedbackWire'):
                self.wires.append(Wire(elem))

        for block in self.blocks.values():
            block.bindWire(self.wires)

        self.topological_sort()

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        with Hierarchy.scope(f"Sheet[{str(self.Number)}]"):
            with PLCFaultHandler.minor():
                for wire in self.wires:
                    wire.Value = None
                ctx.FBD.sheet = self
                if self.execution_order:
                    for block_id in self.execution_order:
                        await self.blocks[block_id].execute(ctx)

    def topological_sort(self):
        depends_on: Dict[int, Set[int]] = {
            bid: set() for bid in self.blocks
        }
        depended_by: Dict[int, List[int]] = {
            bid: [] for bid in self.blocks
        }

        for wire in self.wires:
            if wire.FromID in self.blocks and wire.ToID in self.blocks:
                depends_on[wire.ToID].add(wire.FromID)
                depended_by[wire.FromID].append(wire.ToID)

        queue: List[int] = [
            bid for bid, deps in depends_on.items() if not deps
        ]
        self.execution_order = []

        while queue:
            queue.sort(key=lambda bid: (self.blocks[bid].Y, self.blocks[bid].X))
            current = queue.pop(0)
            self.execution_order.append(current)

            for dependent in depended_by.get(current, []):
                depends_on[dependent].discard(current)
                if not depends_on[dependent]:
                    queue.append(dependent)

        if len(self.execution_order) != len(self.blocks):
            raise RuntimeWarning("Sheet: Circular dependency detected!")

class FBDExecutionContext:
    def __init__(self, sheet: Sheet):
        self.sheet = sheet
        self.temp_store: Dict[str, Any] = {}
        self.RungStatus = True

    def get_wire_value(self, wire: Wire) -> Any:
        source = self.sheet.blocks.get(wire.FromID)
        if source._Type in ('IRef', 'ORef'):
            return getMemory(source.Operand)
        elif source._Type == 'Function':
            key = f"{source.ID}:{wire.FromParam}"
            return self.temp_store.get(key, 0)
        return 0

    def resolve_inputs(self, block: FBDBlock, wires: list[Wire]) -> Dict[str, Any]:
        bound = {}
        for wire in self.sheet.wires:
            if wire.ToID == block.ID:
                bound[wire.ToParam] = self.get_wire_value(wire)
        return bound