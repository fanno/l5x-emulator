from datatypes.custom.datavariant import DataVariant

def split_to_dint(value: int|DataVariant) -> list[int]:
    if isinstance(value, DataVariant):
        value = value.getPLCValue()

    low_mask = 0xFFFFFFFF

    low = value & low_mask

    high = (value >> 32) & low_mask

    def to_signed_32(x: int) -> int:
        return x if x < 0x80000000 else x - 0x100000000

    low_signed  = to_signed_32(low)
    high_signed = to_signed_32(high)

    return [low_signed, high_signed]

def _mask(width: int) -> int:
    return (1 << width) - 1

def AND(a: int, b: int, width: int = 32) -> int:
    return (a & b) & _mask(width)

def OR(a: int, b: int, width: int = 32) -> int:
    return (a | b) & _mask(width)

def XOR(a: int, b: int, width: int = 32) -> int:
    return (a ^ b) & _mask(width)

def NOT(a: int, width: int = 32) -> int:
    return (~a) & _mask(width)