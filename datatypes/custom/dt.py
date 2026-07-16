from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Any

from asyncua import ua
import re

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.compare import COMPARE

from datatypes.custom.math import MATH

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

@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class DT(COMPARE, MATH, DataVariant):
    _value:datetime = field(init=True, repr=False, default_factory=lambda: datetime.now(timezone.utc))

    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.DateTime)
    _py_variant:Any = field(init=False, repr=False, default=int)
    
    def __post_init__(self):
        self.setValue(self._value)

    def getPLCValue(self) -> int:
        utc_dt = self._value.replace(tzinfo=timezone.utc)
        return int(utc_dt.timestamp() * 1000000)
    
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
        us_formatted = f"{us_padded[:3]}_{us_padded[3:]}"

        #return f"DT#{dt_str}.{us_formatted}Z"
        return f"DT#{dt_str}.{us_formatted}({tz_str})"

    @classmethod
    def toValue(self, value:datetime|int|str):
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
                microsecond = int(millis) * 1_000 + int(micros)

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
            if value < 0:
                value = abs(value)
            result = datetime.fromtimestamp(value)

            result = result.replace(tzinfo=timezone.utc)
            return result
        elif isinstance(value, int):
            if value < 0:
                value = abs(value)
            seconds = value // 1_000_000
            remainder = value % 1_000_000
                
            result = datetime.fromtimestamp(seconds).replace(microsecond=remainder)

            result = result.replace(tzinfo=timezone.utc)
            return result

        raise ValueError(f"value '{value}' is not a valid DateTime format")
    
@DataTypeRegistry.register
@dataclass(repr=False, eq=False)
class LDT(COMPARE, DataVariant):
    pass