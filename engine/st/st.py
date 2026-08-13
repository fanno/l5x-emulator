import re

from lxml.etree import _Element as Element

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
            # for debugging
            #print("------------")
            #print("normalizeST:", result)
            result = self.createPython(result)
            #print("createPython:", result)
            #print("------------")
            if isReturn:
                result = "return " + result
            return make_async_st(result)
        except Exception as e:
            raise AssertionError(f"Parsing Error: {result}").with_traceback(e.__traceback__)

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
        clean   = []
        for raw in lines:
            raw = raw.lstrip()

            clean.append(raw)

        full_text = "\n".join(clean)

        output = []
        in_string = False
        comment_type = None

        i = 0
        n = len(full_text)
        while i < n:
            ch = full_text[i]

            if not comment_type:
                if ch == "'":
                    in_string = not in_string

                    output.append(ch)
                    i += 1
                    continue
                if in_string:
                    output.append(ch)
                    i += 1
                    continue
           
            if comment_type:
                if comment_type == '//':
                    if ch == '\n':
                        comment_type = None
                else:
                    end_marker = '*)' if comment_type == '(*' else '*/'
                    if full_text[i:i+2] == end_marker:
                        comment_type = None
                        i += 2
                        continue
                i += 1
                continue

            if full_text[i:i+2] == '//':
                comment_type = '//'
                i += 2
                continue
            
            if full_text[i:i+2] in ('(*', '/*'):
                comment_type = full_text[i:i+2]
                i += 2
                continue

            if full_text[i:i+2] == ':=':
                output.append(' =')
                i += 2
                continue

            skip = False
            rest = full_text[i:]

            #r'(?<!\w)if(?!\w).*?(?<![\w0-9])then(?!\w)',
            #r'(?<!\w)case(?!\w).*?[\s)\]]+(?!\w)',
            patterns = [
                r'(?<!\w);(?!\w)',
                r'(?<!\w):(?![:=\w])',
                r'(?<!\w)end_while.*?[;](?!\w)',
                r'(?<!\w)end_case.*?[;](?!\w)',
                r'(?<!\w)end_for.*?[;](?!\w)',
                r'(?<!\w)end_if.*?[;](?!\w)',
                r'(?<!\w)if(?!\w).*?[\s)\]0-9]+then(?!\w)',
                r'(?<!\w)elsif(?!\w).*?[\s)\]0-9]+then(?!\w)',
                r'(?<!\w)else(?!\w)',
                r'(?<!\w)case(?!\w).*?[\s)\]]+of(?!\w)',
                r'(?<!\w)while(?!\w).*?[\s)\]0-9]+do(?!\w)',
                r'(?<!\w)for(?!\w).*?[\s)\]0-9]+do(?!\w)'
            ]
            
            for pattern in patterns:
                match = re.match(pattern, rest, flags=re.IGNORECASE | re.DOTALL)
                if match:
                    add = full_text[i:i + match.end()].strip()
                    add = add.replace(":=", " =")
                    add = add.replace("\n", " ")
                    #add = add.replace("\t", " ")
                    add = add.strip()
                    output.append(f"{add}\n")
                    i += match.end() + 1
                    skip = True
                    break
            if skip:
                continue

            output.append(ch)
            i += 1

        result = "".join(output)

        return result