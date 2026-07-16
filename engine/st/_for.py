import logging
import re

from engine.st.st import ST
from engine.st.helper import hook_expression

RE_FOR = re.compile(
    r"^\s*for\s+([\w][\w\.\[\]]*)\s*=\s*(.*?)\s+to\s+(.*?)\s+do\s*$",
    re.I
)

RE_FOR_BY = re.compile(
    r"^\s*for\s+([\w\.\[\]]+)\s*=\s*(.*?)\s+to\s+(.*?)\s+by\s+(.*?)\s+do\s*$",
    re.I
)

RE_END_FOR = re.compile(r"^end_for\s*;?$", re.I)

def FOR(line:str, st:ST):
    line = line.strip()

    m = RE_FOR_BY.match(line)
    if m:
        var, start, end, step = m.groups()
        return addFor(st, var, start, end, hook_expression(step))

    m = RE_FOR.match(line)
    if m:
        var, start, end = m.groups()
        return addFor(st, var, start, end, 1)
    
    if RE_END_FOR.match(line):
        st.block_stack.pop()
        st.removeIndent()
        return True

    return False

def addFor(st:ST, var, start, end, step) -> bool:
    st.block_stack.append("FOR")
    start = hook_expression(start)
    end = hook_expression(end)

    st.out.append(
        st.getIndent() +
        f'for {var} in range({start}, {end} + 1, {step}):'
    )
    st.addIndent()
    return True