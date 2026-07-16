from dataclasses import dataclass, field

from asyncua import Node, ua

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.helper import getVariantValue

from core.memory.memory import Memory

from opcua.helpers import createVariant

@dataclass
class Signal:
    PATH:str = field(init=True)
    NODE:Node = field(init=True)
    LAST_VALUE:ua.Variant = field(init=False, default=None)

    def __post_init__(self):
        if isinstance (self.PATH, list):
            self.PATH = ".".join(self.PATH)

async def updateSignal(signal:Signal, memory:Memory):
    if memory.needMemoryUpdate(signal.PATH):
        value = memory.get(signal.PATH)
        if value is not None:
            if isinstance(value, DataVariant):
                await signal.NODE.write_value(value.toVariant())
            else:
                variant_type = await signal.NODE.read_data_type_as_variant_type()
                match variant_type:
                    case ua.VariantType.ExtensionObject:
                        await signal.NODE.write_value(ua.Variant(Value=getVariantValue(value), VariantType=ua.VariantType.ExtensionObject))
                    case _:
                        await signal.NODE.write_value(createVariant(value, variant_type))

def updateMemory(signal: Signal, memory:Memory):
    if isinstance(signal.LAST_VALUE, ua.Variant):
        curentValue = memory.get(signal.PATH)
        if isinstance(curentValue, DataVariant):
            curentValue.fromVariant(signal.LAST_VALUE)
        else:
            memory.set(signal.PATH, signal.LAST_VALUE.Value)
        signal.LAST_VALUE = None