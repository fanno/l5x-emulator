import re

from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from engine.st._while import WHILE
from engine.st._if import IF
from engine.st._for import FOR
from engine.st._case import CASE
from engine.st._call import CALL

from engine.st.helper import hook_assignment, hook_expression

@dataclass
class ST:
    _Element:Element = field(init=True)

    _indent:int = field(init=False, default=0)
    out:list[str] = field(init=False, default_factory=list)
    lines:list[str] = field(init=False, default_factory=list)
    block_stack:list[str] = field(init=False, default_factory=list)

    INDENT_SIZE:int = 4

    def __post_init__(self):
        self.block_stack = []
        self.lines = []
        if isinstance(self._Element, Element):
            for line in self._Element.findall("./Line"):
                self.lines.append(line.text.strip())

    def getPython(self, isReturn:bool = False):
        try:
            from engine.st.hooks import make_async_st

            result = ST.normalizeST(self.lines)
            result = self.createPython(result)
            if isReturn:
                result = "return " + result
            return make_async_st(result)
        except Exception as e:
            raise AssertionError(f"Parsing Error: {self.Name}").with_traceback(e.__traceback__)

    def addIndent(self, amount:int=1) -> None:
        self._indent += (self.INDENT_SIZE * amount)

    def removeIndent(self, amount:int=1) -> None:
        self._indent -= (self.INDENT_SIZE * amount)

    def getIndent(self) -> str:
        return " " * self._indent

    def createPython(self, code: str) -> str:
        lineNum = 1
        self.out:list[str] = []

        for raw in code.splitlines():
            
            line = raw.strip()
            if not line:
                continue

            lineNum += 1

            line = line.replace(":=", "=")

            if CASE(line, self):
                continue

            if WHILE(line, self):
                continue

            if FOR(line, self):
                continue

            if IF(line, self):
                continue

            if CALL(line, self):
                continue

            # assignment / statement
            if line.endswith(";"):
                line = line[:-1]

            if "=" in line:
                self.out.append(self.getIndent() + hook_assignment(line))
            else:
                self.out.append(self.getIndent() + hook_expression(line))

        return "\n".join(self.out)

    @staticmethod
    def normalizeST(lines:list[str]):
        statements = []
        buffer = []
        terminators = ("THEN", "DO", "OF", "ELSE", ";", ":")

        in_block_comment = False

        for raw in lines:
            if in_block_comment:
                match = re.search(r'\*\)', raw)
                if match:
                    raw = raw[match.end():]
                    in_block_comment = False
                else:
                    continue

            raw = re.sub(r"//[^\n]*", '', raw)
            raw = re.sub(r'\(\*.*?\*\)', '', raw, flags=re.DOTALL)

            if '(*' in raw:
                parts = raw.split('(*', 1)
                raw = parts[0]
                in_block_comment = True

            line = raw.strip()
            
            if not line:
                continue

            buffer.append(line)

            joined = " ".join(buffer)
            upper = joined.upper()

            if any(upper.endswith(t) or t in upper for t in terminators):
                statements.append(joined)
                buffer = []

        if buffer:
            statements.append(" ".join(buffer))

        return "\n".join(statements)