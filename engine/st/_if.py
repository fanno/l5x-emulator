import re

from engine.st.st import ST
from engine.st.helper import hook_expression

RE_IF = re.compile(r"^if\s+(.*?)\s+then$", re.I)
RE_ELSIF = re.compile(r"^elsif\s+(.*?)\s+then$", re.I)
RE_ELSE = re.compile(r"^else$", re.I)
RE_END_IF = re.compile(r"^end_if\s*;?$", re.I)

def IF(line:str, st:ST) -> bool:
    m = RE_IF.match(line)
    if m:
        st.block_stack.append("IF")
        st.out.append(st.getIndent() + f"if {hook_expression(m.group(1))}:")
        st.addIndent()
        return True

    m = RE_ELSIF.match(line)
    if m:
        st.removeIndent()
        st.out.append(st.getIndent() + f"elif {hook_expression(m.group(1))}:")
        st.addIndent()
        return True

    if RE_ELSE.match(line):
        st.removeIndent()
        st.out.append(st.getIndent() + "else:")
        st.addIndent()
        return True

    if RE_END_IF.match(line):
        st.removeIndent()
        st.block_stack.pop()
        return True
    
    return False