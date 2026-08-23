import re

import engine.st.st

RE_CALL = re.compile(
    r"^([A-Za-z_]\w*)\s*\((.*)\)\s*;?$",
    re.I
)

RE_CALL_ASSIGN = re.compile(
    r"^(.+?)\s*=\s*([A-Za-z_]\w*)\s*\((.*)\)\s*;?$",
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
    paren_depth  = 0
    bracket_depth = 0

    for ch in arg_str:
        if ch == "," and paren_depth  == 0 and bracket_depth  == 0:
            args.append("".join(current).strip())
            current = []
            continue

        if ch == "(":
            paren_depth  += 1
        elif ch == ")":
            paren_depth  -= 1
        elif ch == "[":
            bracket_depth += 1
        elif ch == "]":
            bracket_depth -= 1

        current.append(ch)

    if current:
        args.append("".join(current).strip())

    return args

def format_call_arg(arg, st):
    arg = arg.strip()

    # Nested function call
    nested_call = format_call(arg, st)
    if nested_call is not None:
        return nested_call

    # Number → pass as-is
    if NUMBER_RE.fullmatch(arg):
        return arg

    # Variable → get()
    #if VAR_PATTERN.fullmatch(arg):
    #    return f'get("{arg}")'

    # Everything else → string literal
    escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'

def format_call(expr: str, st) -> str | None:
    m = RE_CALL.fullmatch(expr.strip())

    if not m:
        return None

    func_name, arg_str = m.groups()

    raw_args = split_args(arg_str) if arg_str.strip() else []

    formatted_args = [
        format_call_arg(arg, st)
        for arg in raw_args
    ]

    return (
        f'await call("{func_name}", '
        f'[{", ".join(formatted_args)}])'
    )


def CALL(line, st:"engine.st.st.ST"):
    m = RE_CALL.match(line)
    if m:
        func_name, arg_str = m.groups()

        raw_args = split_args(arg_str) if arg_str.strip() else []

        formatted_args = [
            format_call_arg(arg, st) for arg in raw_args
        ]

        st.out.append(
            st.getIndent() +
            f'await call("{func_name}", [{", ".join(formatted_args)}])'
        )
        
        return True

    m = RE_CALL_ASSIGN.match(line)
    if m:
        lhs, func_name, arg_str = m.groups()

        raw_args = split_args(arg_str) if arg_str.strip() else []

        formatted_args = [
            format_call_arg(arg, st) for arg in raw_args
        ]

        st.out.append(
            st.getIndent() +
            f'set_("{lhs.strip()}", await call("{func_name}", [{", ".join(formatted_args)}]))'
        )

        return True

    return False

'''
def format_call_arg(arg):
    # Number → pass as-is
    if NUMBER_RE.match(arg):
        return arg

    # Everything else → string literal
    escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
'''
