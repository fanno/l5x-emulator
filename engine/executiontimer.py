import time

from datatypes.custom.numbers import DINT, LINT

class ExecutionTimer:
    start:float = 0
    end:float = 0
    elapsed:float = 0
    ms:int = 0
    μs:int = 0

    def __init__(self):
        self.start = 0
        self.end = 0
        self.elapsed = 0
        self.ms = 0
        self.μs = 0

    def __enter__(self):
        self._enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exit()
        return False

    def __aenter__(self):
        self._enter()
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self._exit()
        return False

    def _enter(self):
        self.start = time.monotonic()

    def _exit(self):
        self.end = time.monotonic()
        self.elapsed = self.end - self.start
        self.ms = int(self.elapsed * 1000)
        self.μs = int(self.elapsed * 1000000)

    @staticmethod
    def get_ms() -> DINT:
        return DINT(ExecutionTimer.get(1000))

    @staticmethod
    def get_μs() -> LINT:
        return LINT(ExecutionTimer.get())

    @staticmethod
    def get(factor:int=1000000) -> int:
        return int(time.monotonic() * factor)