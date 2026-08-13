from datetime import datetime, timedelta
import time

from datatypes.custom.array import Array
from datatypes.custom.numbers import DINT

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

class PLCClock:
    _base:float
    _utc:datetime

    def __init__(self, initial_time: Array[DINT] | None = None, timezone_name: str | None = None, ):
        if initial_time is None:
            self._utc = datetime.now(timezone.utc)
        else:
            self._utc = self._from_array(initial_time).replace(
                tzinfo=timezone.utc
            )

        self._base = time.monotonic()

        if timezone_name is None:
            self._timezone = datetime.now().astimezone().tzinfo
        else:
            self._timezone = ZoneInfo(timezone_name)

    def get_utc(self) -> list[int]:
        return self._to_array(self._get_utc())

    def get_local(self) -> list[int]:
        return self._to_array(self._get_utc().astimezone(self._timezone))

    def set_utc(self, value: list[int]) -> None:
        self._utc = self._from_array(value).replace(
            tzinfo=timezone.utc
        )
        self._base = time.monotonic()

    def get_timezone(self) -> str:
        return self._timezone.key

    def set_timezone(self, timezone_name: str) -> None:
        self._timezone = ZoneInfo(timezone_name)

    def _get_utc(self) -> datetime:
        elapsed = time.monotonic() - self._base
        return self._utc + timedelta(seconds=elapsed)

    @staticmethod
    def _from_array(value: Array[DINT]) -> datetime:
        if len(value) != 7:
            raise ValueError(
                f"WallClockTime requires 7 values, got {len(value)}"
            )

        return datetime(
            year=value[0].getPLCValue(),
            month=value[1].getPLCValue(),
            day=value[2].getPLCValue(),
            hour=value[3].getPLCValue(),
            minute=value[4].getPLCValue(),
            second=value[5].getPLCValue(),
            microsecond=value[6].getPLCValue(),
        )

    @staticmethod
    def _to_array(value: datetime) -> list[int]:
        return [
            DINT(value.year),
            DINT(value.month),
            DINT(value.day),
            DINT(value.hour),
            DINT(value.minute),
            DINT(value.second),
            DINT(value.microsecond),
        ]