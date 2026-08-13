import re

import engine.st.st
from engine.st.helper import hook_expression

RE_IF = re.compile(r"^if(\s*.*?[\s)\]0-9]+)then$", re.I)
RE_ELSIF = re.compile(r"^elsif(\s*.*?[\s)\]0-9]+)then$", re.I)
RE_ELSE = re.compile(r"^else$", re.I)
RE_END_IF = re.compile(r"^end_if\s*;?$", re.I)

def IF(line:str, st:"engine.st.st.ST") -> bool:
    m = RE_IF.match(line)
    if m:
        st.block_stack.append("IF")
        st.out.append(st.getIndent() + f"if {hook_expression(m.group(1).strip())}:")
        st.addIndent()
        return True

    if line.lower().startswith("if "):
        raise SyntaxError(f"if not matched: {line}")

    m = RE_ELSIF.match(line)
    if m:
        st.removeIndent()
        st.out.append(st.getIndent() + f"elif {hook_expression(m.group(1).strip())}:")
        st.addIndent()
        return True

    if line.lower().startswith("elsif "):
        raise SyntaxError(f"elsif not matched: {line}")

    if RE_ELSE.match(line):
        st.removeIndent()
        st.out.append(st.getIndent() + "else:")
        st.addIndent()
        return True

    if RE_END_IF.match(line):
        if not (st.block_stack and st.block_stack[-1] == "IF"):
            raise SyntaxError("end_if without matching IF")
        st.removeIndent()
        st.block_stack.pop()
        return True

    if line.lower().startswith("end_if "):
        raise SyntaxError(f"end_if not matched: {line}")
    
    return False