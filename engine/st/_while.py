import re

import engine.st.st

from engine.st.helper import hook_expression

RE_WHILE = re.compile(r"^while(\s*.*?\s*)do$", re.I)
RE_END_WHILE = re.compile(r"^end_while\s*;?$", re.I)

def WHILE(line:str, st:"engine.st.st.ST"):
    m = RE_WHILE.match(line)
    if m:
        st.block_stack.append("WHILE")
        st.out.append(st.getIndent() + f"while {hook_expression(m.group(1).strip())}:")
        st.addIndent()
        return True

    if line.lower().startswith("while "):
        raise SyntaxError(f"while not matched: {line}")

    if RE_END_WHILE.match(line):
        st.block_stack.pop()
        st.removeIndent()
        return True

    if line.lower().startswith("end_while "):
        raise SyntaxError(f"end_while not matched: {line}")
    
    return False