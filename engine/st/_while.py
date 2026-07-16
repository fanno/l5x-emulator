import re

from engine.st.st import ST
from engine.st.helper import hook_expression

RE_WHILE = re.compile(r"^while\s+(.*?)\s+do$", re.I)
RE_END_WHILE = re.compile(r"^end_while\s*;?$", re.I)

def WHILE(line:str, st:ST):
    m = RE_WHILE.match(line)
    if m:
        st.block_stack.append("WHILE")
        st.out.append(st.getIndent() + f"while {hook_expression(m.group(1))}:")
        st.addIndent()
        return True

    if RE_END_WHILE.match(line):
        st.block_stack.pop()
        st.removeIndent()
        return True
    
    return False