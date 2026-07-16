import re

from engine.st.st import ST

RE_CALL = re.compile(
    r"^([A-Za-z_]\w*)\s*\((.*)\)\s*;?$",
    re.I
)

NUMBER_RE = re.compile(r"""
    ^[+-]?(
        (\d+\.\d*) |
        (\d*\.\d+) |
        (\d+)
    )$
""", re.X)

def split_args(arg_str):
    args = []
    current = []
    depth = 0

    for ch in arg_str:
        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        current.append(ch)

    if current:
        args.append("".join(current).strip())

    return args

def format_call_arg(arg):
    # Number → pass as-is
    if NUMBER_RE.match(arg):
        return arg

    # Everything else → string literal
    escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'

def CALL(line, st:ST):
    m = RE_CALL.match(line)
    if m:
        func_name, arg_str = m.groups()

        raw_args = split_args(arg_str) if arg_str.strip() else []

        formatted_args = [
            format_call_arg(arg) for arg in raw_args
        ]

        st.out.append(
            st.getIndent() +
            f'await call("{func_name}", [{", ".join(formatted_args)}])'
        )
        
        return True

    return False