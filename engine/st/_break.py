import re

import engine.st.st
from engine.st.helper import hook_expression

RE_BREAK = re.compile(r"^exit\s*;?$", re.I)

def BREAK(line:str, st:"engine.st.st.ST") -> bool:
    m = RE_BREAK.match(line)
    if m:
        st.out.append(st.getIndent() + "break")
        return True

    if line.lower().startswith("EXIT"):
        raise SyntaxError(f"EXIT not matched: {line}")
    
    return False