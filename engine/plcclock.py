import time

import datetime as dt

from zoneinfo import ZoneInfo

import threading

class PLCClock:
    def __init__(self, offset: float = 0.0, tz_name: str = "UTC", force_dst: bool | None = None, ):
        self._offset = float(offset)
        self._tz_name = tz_name
        self._tz = ZoneInfo(self._tz_name)
        self._force_dst = force_dst
        self._lock = threading.RLock()

    def set_timezone(self, tz_name: str) -> None:
        with self._lock:
            self._tz_name = tz_name
            self._tz = ZoneInfo(tz_name)

    @property
    def timezone(self) -> str:
        with self._lock:
            return self._tz_name

    @property
    def dst(self) -> bool:
        with self._lock:
            return self._force_dst

    @dst.setter
    def dst(self, value: bool | None) -> None:
        with self._lock:
            self._force_dst = value

    @property
    def offset(self) -> float:
        with self._lock:
            return self._offset

    @offset.setter
    def offset(self, seconds: float) -> None:
        with self._lock:
            self._offset = float(seconds)

    def _now_timestamp(self) -> float:
        with self._lock:
            return time.time() + self._offset

    def time(self) -> float:
        return self._now_timestamp()

    def utcnow(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(
            self._now_timestamp(), tz=dt.timezone.utc
        )

    def now(self, tz: dt.tzinfo | None = None) -> dt.datetime:
        with self._lock:
            chosen_tz = tz or self._tz

        base_dt = dt.datetime.fromtimestamp(self._now_timestamp(), tz=dt.timezone.utc)

        zoned = base_dt.astimezone(chosen_tz)

        if self._force_dst is not None:
            jan1 = dt.datetime(base_dt.year, 1, 1, tzinfo=chosen_tz)
            std_offset = jan1.utcoffset()

            cur_offset = zoned.utcoffset()

            desired_offset = std_offset + (dt.timedelta(hours=1) if self._force_dst else dt.timedelta(0))

            delta = desired_offset - cur_offset
            zoned = zoned + delta

        return zoned

    def isoformat(self, tz: dt.tzinfo | None = None) -> str:
        return self.now(tz).isoformat()