import ast
import re

class L5KReader:
    def __init__(self, data: str|list):
        if isinstance(data, str):
            self.data = self._parse(data)
        elif isinstance(data, list):
            self.data = data
        elif isinstance(data, int):
            self.data = data
        else:
            raise TypeError(f"data must be str or list, not {type(data).__name__}")

        self.index = -1
        self.bit_index = 0

    @staticmethod
    def _parse(data: str) -> list:
        data = re.sub(
            r'\b(\d+)#([0-9A-Fa-f_]+)\b',
            lambda m: str(int(m.group(2).replace("_", ""), int(m.group(1)))),
            data,
            flags=re.I,
        )

        value = ast.literal_eval(data)
        return value

    def _next(self):
        self.index += 1
        self.bit_index = 0
        return self._current()

    def _current(self):
        if isinstance(self.data , list):
            return self.data[self.index]
        else:
            return self.data

    def nextRaw(self):
        return self._next()

    def nextBool(self):
        if self.index < 0:
            self.index += 1
        if self.bit_index >= 32:
            self.index += 1
            self.bit_index = 0
        print("nextBool", self._current())
        value = bool(self._current() & (1 << self.bit_index))
        self.bit_index += 1

        return value

