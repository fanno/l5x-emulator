import re

import engine.st.st
from engine.st.helper import hook_expression

RE_FOR = re.compile(
    r"^\s*for\s+([\w][\w\.\[\]]*)\s*=\s*(.*?\s*)to\s+(.*?\s*)do\s*$",
    re.I
)

RE_FOR_BY = re.compile(
    r"^\s*for\s+([\w\.\[\]]+)\s*=\s*(.*?\s*)to\s+(.*?\s*)by\s+(.*?\s*)do\s*$",
    re.I
)

RE_END_FOR = re.compile(r"^end_for\s*;?$", re.I)

def FOR(line:str, st:"engine.st.st.ST"):
    line = line.strip()


    m = RE_FOR_BY.match(line)
    if m:
        var, start, end, step = m.groups()
        return addFor(st, var.strip(), start.strip(), end.strip(), hook_expression(step.strip()))

    m = RE_FOR.match(line)
    if m:
        var, start, end = m.groups()
        return addFor(st, var.strip(), start.strip(), end.strip(), 1)

    if line.lower().startswith("for "):
        raise SyntaxError(f"for not matched: {line}")
    
    if RE_END_FOR.match(line):
        if not (st.block_stack and st.block_stack[-1] == "FOR"):
            raise SyntaxError("end_for without matching FOR")
        st.block_stack.pop()
        st.removeIndent()
        return True

    if line.lower().startswith("end_for "):
        raise SyntaxError(f"end_for not matched: {line}")

    return False

def addFor(st:"engine.st.st.ST", var:str, start, end, step) -> bool:
    st.block_stack.append("FOR")
    start = hook_expression(start)
    end = hook_expression(end)

    var_rep = var.replace(".", "_")
    # TODO: arrays[0,3] would also break here?

    st.out.append(
        st.getIndent() +
        f'for {var_rep} in range({start}, {end} + 1, {step}):'
    )
    st.addIndent()
    
    st.out.append(
        st.getIndent() +
        f'set_("{var}", {var_rep})'
    )

    return True