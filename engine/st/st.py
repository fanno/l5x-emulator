import re

from lxml.etree import _Element as Element

from dataclasses import dataclass, field, InitVar

from engine.st._while import WHILE
from engine.st._if import IF
from engine.st._for import FOR
from engine.st._case import CASE
from engine.st._call import CALL
from engine.st._break import BREAK

from engine.st.helper import hook_assignment, hook_expression

@dataclass
class ST:
    element: InitVar[Element]

    _indent:int = field(init=False, default=0)
    out:list[str] = field(init=False, default_factory=list)
    lines:list[str] = field(init=False, default_factory=list)
    block_stack:list[str] = field(init=False, default_factory=list)

    INDENT_SIZE:int = 4

    def __post_init__(self, element:Element):
        self.block_stack = []
        self.lines = []
        if isinstance(element, Element):
            for line in element.findall("./Line"):
                self.lines.append(line.text.strip())

    def getPython(self, isReturn:bool = False, doPrint=False):
        try:
            from engine.st.hooks import make_async_st
            result = ST.normalizeST(self.lines)

            if result.find('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') > -1:
                print("-3-----------------------------------------------------------------------------------------------------------")
                print(result)

            # for debugging
            #print("------------")
            #print("normalizeST:", result)
            result = self.createPython(result)
            #print("createPython:", result)
            #print("------------")
            if isReturn:
                result = "return " + result

            if result.find('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') > -1:
                print("-4-----------------------------------------------------------------------------------------------------------")
                print(result)

            #return make_async_st(result)



            expression = make_async_st(result)

            if doPrint:
                print(expression)

            # Compile to bytecode object (not just string)
            compiled = compile(
                expression,
                filename=f"<ST>", 
                mode='exec'
            )
            return compiled
        
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
            if BREAK(line, self):
                continue

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
    def normalize_radix(match: re.Match) -> str:
        base = int(match.group(1))
        value = match.group(2).replace("_", "")

        if base == 2:
            return f"0b{value}"
        if base == 8:
            return f"0o{value}"
        if base == 16:
            return f"0x{value}"

        raise ValueError(f"Unsupported radix: {base}")

    @staticmethod
    def normalizeST(lines:list[str]):
        clean   = []
        for raw in lines:
            raw = re.sub(r'[\r\n\t]', ' ', raw)
            raw = raw.strip()
            clean.append(raw)

        full_text = "\n".join(clean)

        output = []
        in_string = False
        comment_type = None

        #remove comments
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

            output.append(ch)
            i += 1

        full_text = "".join(output)

        RADIX_RE = re.compile(
            r'\b(2|8|16)#([0-9A-Fa-f_]+)\b',
            re.I
        )

        full_text = RADIX_RE.sub(ST.normalize_radix, full_text)
        full_text = re.sub(r"\bXOR\b", "^", full_text, flags=re.I)

        if full_text.find('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') > -1:
            print("-1-----------------------------------------------------------------------------------------------------------")
            print(full_text)

        full_text = re.sub(r'[\r\n\t]', ' ', full_text)

        if full_text.find('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') > -1:
            print("-2-----------------------------------------------------------------------------------------------------------")
            print(full_text)

        output = []
        i = 0
        n = len(full_text)
        while i < n:
            ch = full_text[i]

            skip = False
            rest = full_text[i:]

            #r'(?<!\w)if(?!\w).*?(?<![\w0-9])then(?!\w)',
            #r'(?<!\w)case(?!\w).*?[\s)\]]+(?!\w)',
            #r'^if(?!\w).*?[\s)\]0-9]+then\b',
            patterns = [
                r'^[\s]*?exit\s*[;](?!\w)',
                r'^[\s]*?end_while\s*[;](?!\w)',
                r'^[\s]*?end_case\s*[;](?!\w)',
                r'^[\s]*?end_for\s*[;](?!\w)',
                r'^[\s]*?end_if\s*[;](?!\w)',
                r'^[\s]*?elsif(?!\w).*?[\s)\]0-9]+then\b',
                r'^[\s]*?if[\s\(].*?[\s\)\]0-9]+then\b',
                r'^[\s]*?else(?!\w)',
                r'^[\s]*?case(?!\w).*?[\s)\]]+of\b',
                r'^[\s]*?while(?!\w).*?[\s)\]0-9]+do\b',
                r'^[\s]*?for(?!\w).*?[\s)\]0-9]+do\b',
                r'^[0-9#abcdefxo\.\,\s]*?:(?![:=])',
                r'^.*?;'
            ]
            
            for pattern in patterns:
                match = re.match(pattern, rest, flags=re.IGNORECASE | re.DOTALL)
                if match:
                    add = full_text[i:i + match.end()].strip()
                    add = add.replace(":=", " =")
                    add = re.sub(r'[\r\n\t]', ' ', add)
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