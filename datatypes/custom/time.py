from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar
import re

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant

from datatypes.custom.numbers import DINT, LINT

_TIME_PATTERN = re.compile(
    r"^(?P<type>T32|T|LT)#"
    r"(?P<sign>[+-])?"
    r"(?:(?P<days>\d+)d)?"
    r"(?:(?P<hours>\d+)h)?"
    r"(?:(?P<minutes>\d+)m)?"
    r"(?:(?P<seconds>\d+)s)?"
    r"(?:(?P<millis>\d+)ms)?"
    r"(?:(?P<micros>\d+)us)?"
    r"$",
    re.IGNORECASE,
)

@dataclass
class RELATIVETIME(DataVariant):
    _prefix: ClassVar[str] = ""
    _units_per_second: ClassVar[int] = 1000000

    _py_variant: ClassVar[type] = int
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.UInt64

    _value:LINT = field(init=True, repr=False, default_factory=LINT)
    
    def toString(self):
        value = self._value.getPLCValue()

        sign = "-" if value < 0 else ""
        value = abs(value)

        units_per_second = self._units_per_second

        seconds, remainder = divmod(value, units_per_second)

        days, seconds = divmod(seconds, 86_400)
        hours, seconds = divmod(seconds, 3_600)
        minutes, seconds = divmod(seconds, 60)

        if units_per_second == 1000000:
            milliseconds, microseconds = divmod(remainder, 1000)
            fractions = []

            if milliseconds:
                fractions.append(f"{milliseconds}ms")
            if microseconds:
                fractions.append(f"{microseconds}us")

        elif units_per_second == 1000000000:
            milliseconds, remainder = divmod(remainder, 1000000)
            microseconds, nanoseconds = divmod(remainder, 1000)

            fractions = []

            if milliseconds:
                fractions.append(f"{milliseconds}ms")
            if microseconds:
                fractions.append(f"{microseconds}us")
            if nanoseconds:
                fractions.append(f"{nanoseconds}ns")

        else:
            raise ValueError(
                f"Unsupported relative time resolution: {units_per_second}"
            )

        parts = []

        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds:
            parts.append(f"{seconds}s")

        parts.extend(fractions)

        if not parts:
            parts.append("0s")

        return f"{self._prefix}#{sign}{'_'.join(parts)}"

    @classmethod
    def toValue(cls, value: int | str):
        value = super().toValue(value)

        if isinstance(value, str):
            value = value.strip()

            m = _TIME_PATTERN.match(value)
            if m:
                days = int(m["days"] or 0)
                hours = int(m["hours"] or 0)
                minutes = int(m["minutes"] or 0)
                seconds = int(m["seconds"] or 0)
                millis = int(m["millis"] or 0)
                micros = int(m["micros"] or 0)
                nanos = int(m["nanos"] or 0)

                result = (
                    days * 86_400
                    + hours * 3_600
                    + minutes * 60
                    + seconds
                )

                result *= cls._units_per_second

                if cls._units_per_second == 1000000:
                    result += millis * 1000
                    result += micros

                elif cls._units_per_second == 1000000000:
                    result += millis * 1000000
                    result += micros * 1000
                    result += nanos

                else:
                    raise ValueError(
                        f"Unsupported relative time resolution: "
                        f"{cls._units_per_second}"
                    )

                if m["sign"] == "-":
                    result = -result

                return result

        elif isinstance(value, int):
            return value

        raise ValueError(f"value '{value}' is not a valid TIME format")
    
@DataTypeRegistry.register
@dataclass
class TIME(RELATIVETIME):
    _prefix: ClassVar[str] = "T"

@DataTypeRegistry.register
@dataclass
class TIME32(RELATIVETIME):
    _value:DINT = field(init=True, repr=False, default_factory=DINT)
    _ua_variant: ClassVar[ua.VariantType] = ua.VariantType.UInt32
    _prefix: ClassVar[str] = "T32"

@DataTypeRegistry.register
@dataclass
class LTIME(RELATIVETIME):
    _prefix: ClassVar[str] = "LT"
    _units_per_second: ClassVar[int] = 1000000000
