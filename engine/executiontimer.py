import time

class ExecutionTimer:
    start = 0
    elapsed = 0

    def __enter__(self):
        self.start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.monotonic() - self.start
        return False

    def getInt(self):
        return int(self.elapsed * 1000000)