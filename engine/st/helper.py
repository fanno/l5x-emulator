import re

STRING_RE = re.compile(r"'(?:\\'|[^'])*'")

KEYWORDS = {
    "if", "elif", "else", "and", "or", "not",
    "True", "False", "None", "check", "get", "set_"
}

VAR_PATTERN = re.compile(
    r"\b([a-zA-Z_][a-zA-Z0-9_:\.]*)"
    r"((?:\.[a-zA-Z_][a-zA-Z0-9_]*)|(?:\[[^\]]+\]))*"
)

def extract_strings(text: str):
    strings = []

    def repl(match:re.Match):
        strings.append(match.group(0))
        return f"__STR_{len(strings)-1}__"

    return STRING_RE.sub(repl, text), strings

def restore_strings(text: str, strings):
    for i, s in enumerate(strings):
        text = text.replace(f"__STR_{i}__", s)
    return text

def normalize_expr(expr: str) -> str:
    expr = expr.replace("<>", "!=")
    expr = re.sub(r"\bAND\b", "and", expr, flags=re.I)
    expr = re.sub(r"\bOR\b", "or", expr, flags=re.I)
    expr = re.sub(r"\bNOT\b", "not", expr, flags=re.I)
    expr = re.sub(r"(?<![<>=!])=(?!=)", "==", expr)
    return expr

def hook_expression(expr: str) -> str:
    expr, strings = extract_strings(expr)

    expr = normalize_expr(expr)

    def repl(m:re.Match):
        full:str = m.group(0)
        root:str = m.group(1)

        if (
            root in KEYWORDS
            or root.isdigit()
            or is_string_placeholder(root)
        ):
            return full

        replaced = full.replace(root, f'get("{root}")', 1)

        replaced = re.sub(
            r"\[([^\]]+)\]",
            lambda x: f"[{hook_expression(x.group(1))}]",
            replaced
        )

        return replaced

    expr = VAR_PATTERN.sub(repl, expr)

    return restore_strings(expr, strings)

def is_string_placeholder(name: str) -> bool:
    return name.startswith("__STR_") and name.endswith("__")

def hook_assignment(line: str) -> str:
    lhs, rhs = map(str.strip, line.split("=", 1))
    return f'set_("{lhs}", {hook_expression(rhs)})'