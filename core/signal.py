from dataclasses import dataclass, field
from typing import Type, TYPE_CHECKING

from asyncua import Node, ua

if TYPE_CHECKING:
    from core.memory.memory import Memory

from opcua.helpers import createVariant

from protocols.opcua import SupportsVariant

from utils.isplcinstance import isPLCInstance

@dataclass
class Signal:
    PATH:str = field(init=True)
    NODE:Node = field(init=True)
    MEMORY:Type = field(init=True)
    LAST_VALUE:ua.Variant = field(init=False, default=None)

    def __post_init__(self):
        if isinstance (self.PATH, list):
            self.PATH = ".".join(self.PATH)

async def updateSignal(signal:Signal, memory:"Memory"):
    if memory.needMemoryUpdate(signal.PATH):
        value = memory.get(signal.PATH)
        if isPLCInstance(value, SupportsVariant):
            await signal.NODE.write_value(value.toVariant())

def updateMemory(signal: Signal, memory:"Memory", forceOpcua:bool=False):
    if isinstance(signal.LAST_VALUE, ua.Variant):
        metadata = memory.get_metadata(signal.PATH)
        if metadata:
            from core.memory.memory import OpcUaAccess
            if metadata.OpcUa_Access == OpcUaAccess.READ_WRITE or forceOpcua:
                curentValue = memory.get(signal.PATH)
                if isPLCInstance(curentValue, SupportsVariant):
                    curentValue.fromVariant(signal.LAST_VALUE)
    signal.LAST_VALUE = None