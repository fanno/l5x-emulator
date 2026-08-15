from dataclasses import dataclass, field
from typing import Type, TYPE_CHECKING

from asyncua import Node, ua

from datatypes.custom.helper import getVariantValue

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
        if value is not None:
            if isPLCInstance(value, SupportsVariant):
                await signal.NODE.write_value(value.toVariant())
            else:
                variant_type = await signal.NODE.read_data_type_as_variant_type()
                match variant_type:
                    case ua.VariantType.ExtensionObject:
                        await signal.NODE.write_value(ua.Variant(Value=getVariantValue(value), VariantType=ua.VariantType.ExtensionObject))
                    case _:
                        await signal.NODE.write_value(createVariant(value, variant_type))

def updateMemory(signal: Signal, memory:"Memory", forceOpcua:bool=False):
    if isinstance(signal.LAST_VALUE, ua.Variant):
        metadata = memory.get_metadata(signal.PATH)
        if metadata:
            from core.memory.memory import OpcUaAccess
            if metadata.OpcUa_Access == OpcUaAccess.READ_WRITE or forceOpcua:
                curentValue = memory.get(signal.PATH)
                if isPLCInstance(curentValue, SupportsVariant):
                    curentValue.fromVariant(signal.LAST_VALUE)
                else:
                    memory.set(signal.PATH, signal.LAST_VALUE.Value)
        signal.LAST_VALUE = None