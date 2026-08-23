from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, InitVar
from typing import ClassVar, Any, Iterator

from asyncua import ua
import re

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.compare import COMPARE
from datatypes.custom.math import MATH
from datatypes.custom.bool import BOOL, MEMORY_BIT


_DT_PATTERN = re.compile(
    r"""
    ^                                   # start of string
    (?:                                 # ── optional “DT#” prefix ──
        DT\#                            # literal “DT#”
    )?
    (?P<year>\d{4})                     # year  (4 digits)
    -
    (?P<month>\d{2})                    # month (01‑12)
    -
    (?P<day>\d{2})                      # day   (01‑31)
    (?:                                 # ── separator ──
        -                               #   dash for the original format
        |
        T                               #   “T” for the ISO‑8601 style
    )
    (?P<hour>\d{2})                     # hour   (00‑23)
    :
    (?P<minute>\d{2})                   # minute (00‑59)
    :
    (?P<second>\d{2})                   # second (00‑59)
    \.
    (?P<millis>\d{3})                   # milliseconds
    (?:                                 # ── optional microseconds (original only) ──
        _
        (?P<micros>\d{3})
    )?
    (?:                                 # ── timezone specifier ──
        Z                               #   UTC “Z”
        |
        $$
        UTC
        (?P<sign>[+-])                  #   sign (+ or -)
        (?P<off_hr>\d{2})               #   offset hours
        :
        (?P<off_min>\d{2})              #   offset minutes
        $$
    )?                                  # timezone part is optional
    $                                   # end of string
    """,
    re.VERBOSE,
)

@dataclass(repr=False, eq=False)
class ABSOLUTETIVETIME(COMPARE, MATH, DataVariant):
    init: InitVar[datetime|int|str] = None
    _value:datetime = field(init=False, repr=False, default_factory=lambda: datetime.now(timezone.utc))

    _py_variant: ClassVar[type] = int
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.DateTime

    _units_per_second: ClassVar[int] = 1000000
    _prefix: ClassVar[str] = ""

    def __post_init__(self, init:Any = None) -> None:
        self.setValue(init)

    def getPLCValue(self) -> int:
        utc_dt = self._value.replace(tzinfo=timezone.utc)
        return int(utc_dt.timestamp() * self._units_per_second)

    def getUAValue(self) -> datetime:
        return self._value

    def toString(self):
        offset = self._value.utcoffset()

        if offset is None:
            offset = timedelta(0)

        total_seconds = int(offset.total_seconds())
        sign = '+' if total_seconds >= 0 else '-'
        abs_seconds = abs(total_seconds)
        hours = abs_seconds // 3600
        minutes = (abs_seconds % 3600) // 60
        
        tz_str = f"UTC{sign}{hours:02d}:{minutes:02d}"

        dt_str = self._value.strftime("%Y-%m-%d-%H:%M:%S")

        us = self._value.microsecond
        us_padded = f"{us:06d}"

        fractions:list[str] = []
        fractions.append(us_padded[:3])
        fractions.append(us_padded[3:])

        fraction = f"{us_padded[:3]}_{us_padded[3:]}"
        if self._units_per_second == 1000000:
            pass
        elif self._units_per_second == 1000000000:
            fractions.append("000")
        else:
            raise ValueError(
                f"Unsupported time resolution: {self._units_per_second}"
            )
        fraction = "_".join(fractions)
        return f"{self._prefix}#{dt_str}.{fraction}({tz_str})"

    @classmethod
    def toValue(cls, value:datetime|int|str):
        value = super().toValue(value)
        if isinstance(value, datetime):
            result = value
            return result
        elif isinstance(value, str):
            value = value.strip()
            m = _DT_PATTERN.match(value)
            if m:
                year   = int(m["year"])
                month  = int(m["month"])
                day    = int(m["day"])
                hour   = int(m["hour"])
                minute = int(m["minute"])
                second = int(m["second"])

                millis = m["millis"]
                micros = m["micros"]
                if micros is None:
                    micros = 0
                microsecond = (int(millis) * 1000) + int(micros)

                if m["sign"]:
                    sign = 1 if m["sign"] == "+" else -1
                    offset = timedelta(
                        hours=int(m["off_hr"]),
                        minutes=int(m["off_min"]),
                    ) * sign
                    tzinfo = timezone(offset)
                else:
                    tzinfo = timezone.utc

                result = datetime(
                    year, month, day,
                    hour, minute, second,
                    microsecond=microsecond,
                    tzinfo=tzinfo,
                )
                return result
        elif isinstance(value, float):
            value = abs(value)
            result = datetime.fromtimestamp(value)
            result = result.replace(tzinfo=timezone.utc)
            return result
        elif isinstance(value, int):
            value = abs(value)
                
            seconds = value // cls._units_per_second
            remainder = value % cls._units_per_second
                
            result = datetime.fromtimestamp(seconds, tz=timezone.utc)
            if cls._units_per_second == 1000000:
                microsecond = remainder
            elif cls._units_per_second == 1000000000:
                microsecond = remainder // 1000
            else:
                raise ValueError(f"Unsupported time resolution: {cls._units_per_second}")
            result = result.replace(microsecond=microsecond)
            return result

        raise ValueError(f"value '{value}', type '{type(value)}' is not a valid DateTime format")

    def __len__(self) -> int:
        return 64

    def __iter__(self) -> Iterator[MEMORY_BIT]:
        for bit_index in range(len(self)):
            yield self[bit_index]

    def __getitem__(self, bit: int) -> MEMORY_BIT:
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= self.getBitSize():
            raise IndexError(f"Bit index {bit} out of range")

        return MEMORY_BIT(self, bit)

    def __setitem__(self, bit: int, value: bool):
        if not isinstance(bit, int):
            raise TypeError("Bit index must be an integer")

        if bit < 0 or bit >= 64:
            raise IndexError(f"Bit index {bit} out of range")

        current = self.getPLCValue()
        if BOOL.toValue(value):
            old |= 1 << bit
        else:
            old &= ~(1 << bit)

        self.setValue(current)            

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class DT(ABSOLUTETIVETIME):
    _prefix: ClassVar[str] = "DT"
    
@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LDT(ABSOLUTETIVETIME):
    _units_per_second: ClassVar[int] = 1000000000
    _prefix: ClassVar[str] = "LDT"
