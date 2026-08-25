import ast
import re

L5KBOOLBYTEEND = "lk5.bool.byte.end"
L5KSKIP = "lk5.skip"

class L5KReader:
    debugging = {}

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
        self.setBitRules(0, 1, 7)

    def setBitRules(self, start:int, step:int, end:int):
        if step == 0:
            raise ValueError("Bit rule step cannot be 0")
        self.bit_step = step
        self.bit_start = start
        self.bit_end = end
        self._resetBit()

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

    def _resetBit(self):
        self.bit_index = self.bit_start - self.bit_step
        self.bool = False

    def _next(self):
        self.index += 1
        self._resetBit()
        return self._current()

    def _current(self):
        if isinstance(self.data , list):
            return self.data[self.index]
        else:
            return self.data

    def nextRaw(self):
        return self._next()

    def nextBoolByte(self):
        self.bool = False
        
    def nextBool(self):
        if not self.bool:
            self.index += 1
        
        self.bit_index += self.bit_step

        if self.bit_step > 0:
            if self.bit_index > self.bit_end:
                if self.bool:
                    self.index += 1
                self.bit_index = self.bit_start
        else:
            if self.bit_index < self.bit_end:
                if self.bool:
                    self.index += 1
                self.bit_index = self.bit_start
        self.bool = True
        
        return bool(self._current() & (1 << self.bit_index))