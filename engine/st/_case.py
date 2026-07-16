import re

from engine.st.st import ST
from engine.st.helper import hook_expression, hook_assignment

RE_CASE = re.compile(r"^case\s+(.*?)\s+of$", re.I)
RE_CASE_ITEM = re.compile(r"^(.*?):$")
RE_END_CASE = re.compile(r"^end_case\s*;?$", re.I)

def CASE(line:str, st:ST) -> bool:
    m = RE_CASE.match(line)
    if m:
        st.block_stack.append("case")
        st.out.append(st.getIndent() + f"match {hook_expression(m.group(1))}:")
        st.addIndent(2)
        return True

    if st.block_stack and st.block_stack[-1] == "case":
        if line.lower() == "else" or line.lower().startswith("else "):
            rest = line[4:].strip() if len(line) > 4 else None

            st.removeIndent()
            st.out.append(st.getIndent() + "case _:")
            st.addIndent()

            if rest:
                rest = rest.rstrip(";").strip()
                st.out.append(st.getIndent() + hook_assignment(rest))
            return True

        m_item = RE_CASE_ITEM.match(line)
        if m_item:
            value:str = m_item.groups()[0].strip()
            numbers = []
            parts = value.split(",")
            for part in parts:
                if ".." in part:
                    start, end = part.split("..")
                    for num in range(int(start.strip()), int(end.strip())):
                        numbers.append(str(num))
                else:
                    numbers.append(part)
            value = "|".join(numbers)

            st.removeIndent()
            st.out.append(st.getIndent() + f"case {value}:")
            st.addIndent()
            return True

    if RE_END_CASE.match(line):
        if not (st.block_stack and st.block_stack[-1] == "case"):
            raise SyntaxError("end_case without matching case")
        st.removeIndent(2)
        st.block_stack.pop()
        return True
    
    return False