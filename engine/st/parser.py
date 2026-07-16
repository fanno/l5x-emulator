from engine.st.st import ST
from engine.st._while import WHILE
from engine.st._if import IF
from engine.st._for import FOR
from engine.st._case import CASE
from engine.st._call import CALL
from engine.st.helper import hook_assignment, hook_expression

import re

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

def createPython(code: str, indent_size: int = 4) -> str:
    parsedST = ST()

    lineNum = 1
    for raw in code.splitlines():
        
        line = raw.strip()
        if not line:
            continue

        lineNum += 1

        line = line.replace(":=", "=")

        if CASE(line, parsedST):
            continue

        if WHILE(line, parsedST):
            continue

        if FOR(line, parsedST):
            continue

        if IF(line, parsedST):
            continue

        if CALL(line, parsedST):
            continue

        # assignment / statement
        if line.endswith(";"):
            line = line[:-1]

        if "=" in line:
            parsedST.out.append(parsedST.getIndent() + hook_assignment(line))
        else:
            parsedST.out.append(parsedST.getIndent() + hook_expression(line))

    return "\n".join(parsedST.out)
   