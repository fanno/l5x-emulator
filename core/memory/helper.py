import ast
import operator
import regex as re
import hashlib

from typing import Any
from enum import Enum, auto

from core.errors import MemoryException

from dataclasses import is_dataclass, fields

from engine.helper import CurrentProgramName, currentAOIMemory
from datatypes.custom.datavariant import DataVariant

from datatypes.custom.array import Array

from core.constants import SYSTEMTAGS, CONTROLLERTAGS

#BASE_OR_DEC_PATTERN = re.compile(
#    r"""^
#        (?:
#            (?P<base>\d+)\#(?P<val>[\w_]+)
#        |
#            (?P<sign>[+-])?
#            (?P<dec>\d[\d_]*\.?\d*|\.\d[\d_]*)
#        )
#        $
#    """,
#    re.VERBOSE,
#)

BASE_OR_DEC_PATTERN = re.compile(
    r"^(?:(?P<base>\d+)#(?P<val>[\w_]+)|(?P<sign>[+-]?)(?P<dec>\d+(?:\.\d+)?(?:[eE][+-]?\d+)?))$"
)

class OutputType(Enum):
    Raw = auto()
    PLC = auto()
    UA = auto()

def strNumber(number:str) -> int | float:
    if isinstance(number, str):
        number = number.replace("_", "")

        m = BASE_OR_DEC_PATTERN.fullmatch(number)
        if not m:
            raise ValueError(
                f"Unsupported numeric format: '{number}'. "
                "Allowed: <base>#<value> (no sign) or signed decimal integer/float "
                "(underscores allowed, no scientific notation)."
            )

        if m.group('base') is not None:
            base = int(m.group('base'))
            if not (2 <= base <= 36):
                raise ValueError(f"Base must be between 2 and 36, got {base}")

            value = m.group('val')

            def _validate_digits_for_base(digits: str, base: int) -> bool:
                allowed = "0123456789"[:base]
                allowed_set = set(allowed)
                return all(ch.lower() in allowed_set for ch in digits)

            if not _validate_digits_for_base(value, base):
                raise ValueError(
                    f"Digits '{value}' are not valid for base {base}"
                )
            return int(value, base)

        sign = m.group('sign') or ''
        value = m.group('dec')

        if '.' in value or 'e' in value.lower():
            return float(sign + value)
        else:
            return int(sign + value)
    else:
        return number

def getHash(obj) -> str:
    return hashlib.sha256(str(obj).encode('utf-8')).hexdigest()

def isBitSet(value: int, index: int) -> bool:
    if not 0 <= index < 64:
        raise ValueError("index must be between 0 and 63 inclusive")
    return (value >> index) & 1 == 1

def isBitIndex(keys:list[str|int]) -> bool:
    return bool(isinstance(keys[-1], str) and keys[-1].isdigit() and len(keys) > 1)

def getValue(container:dict|list|int, key:str|int) -> Any:
    key = resolveKey(container, key)
    if isinstance(container, dict):
        if key is None or key not in container:
            raise KeyError(f"Missing dict key: {key} {container}")
        return container[key]
    elif isinstance(container, (list, Array)):
        if key is None:
            raise IndexError("Leaf key is None for list access")
        return container[key]
    else:
        if key is None or not hasattr(container, key):
            raise AttributeError(f"Missing attribute: {key} {container}")
        return getattr(container, key)

def getMemory(pathRaw:list[str] | str, dataVariant:OutputType=OutputType.Raw):
    result = None
    try:
        if isinstance(pathRaw, str):
            if pathRaw.startswith("\'"):
                return pathRaw[1:-1]
            elif pathRaw[0].isdigit():
                return strNumber(pathRaw)
            elif any(c in pathRaw for c in ['+','-','/','*','%',]):
                result = resolveMathExpr(pathRaw)

        if result is None:
            path:list[str] = resolvePath(pathRaw)
            
            from engine.aoi.memory import AOIMemory
            aoi = currentAOIMemory()
            if isinstance(aoi, AOIMemory):
                if aoi.memory.has(path):
                    result = aoi.memory.get(path)
                else:
                    from core.memory.memory import PlcMemory
                    memory = PlcMemory.getContainer(SYSTEMTAGS)
                    if memory.has(path):
                        result = memory.get(path)
            else:
                from core.memory.memory import PlcMemory
                if path[0].startswith("\\"):
                    program = path[0].lstrip("\\")
                    path.pop(0)
                    memory = PlcMemory.getContainer(program)
                    result = memory.get(path)
                else:
                    name = CurrentProgramName.get()
                    memory = PlcMemory.getContainer(name)
                    if memory and memory.has(path):
                        result = memory.get(path)
                    else:
                        memory = PlcMemory.getContainer(CONTROLLERTAGS)
                        if memory.has(path):
                            result = memory.get(path)
                        else:
                            memory = PlcMemory.getContainer(SYSTEMTAGS)
                            if memory.has(path):
                                result = memory.get(path)

        raw = result
        if isinstance(result, DataVariant):
            match dataVariant:
                case OutputType.PLC:
                    result = result.getPLCValue()
                case OutputType.UA:
                    result = result.getUAValue()
    except Exception as e:
        raise MemoryException("getMemory", pathRaw).with_traceback(e.__traceback__)
    
    if result is None:
        raise MemoryException("getMemory", pathRaw)
    
    return result    

def setMemory(path:list[str] | str, value):
    path = resolvePath(path)
    if value is None:
        raise MemoryException("setMemory", path)
    try:
        if isinstance(path, list):
            from engine.aoi.memory import AOIMemory
            aoi = currentAOIMemory()
            if isinstance(aoi, AOIMemory):
                if aoi.memory.has(path):
                    aoi.memory.set(path, value)
                else:
                    from core.memory.memory import PlcMemory
                    memory = PlcMemory.getContainer(SYSTEMTAGS)
                    if memory.has(path):
                        memory.set(path, value)
            else:
                from core.memory.memory import PlcMemory
                memory = None
                if path[0].startswith("\\"):
                    program = path[0].lstrip("\\")
                    path.pop(0)
                    memory = PlcMemory.getContainer(program)
                else:
                    name = CurrentProgramName.get()
                    memory = PlcMemory.getContainer(name) if name else None

                    if memory is None or not memory.has(path):
                        memory = PlcMemory.getContainer(CONTROLLERTAGS)

                        if memory is None or not memory.has(path):
                            memory = PlcMemory.getContainer(SYSTEMTAGS)

                if memory is not None:
                    memory.set(path, value)
    except Exception as e:
        raise MemoryException("setMemory", path, value).with_traceback(e.__traceback__)

def resolveKey(container, key:str|int):
    if isinstance(key, int):
        return key
    if hasattr(container, key):
        return key

    lowered = {}

    if is_dataclass(container):
        for field in fields(container):
            lowered[field.name.lower()] = field.name
    elif isinstance(container, dict):
        for k, v in container.items():
            if isinstance(k, str):
                lowered[k.lower()] = k
            else:
                lowered[k] = k

    if not lowered:
        return key

    return lowered.get(key.lower(), key)

class Expr: 
    def __init__(self, text: str):
        self.text = text

PATH_RE = re.compile(
    r"""
    [A-Za-z_:\\][A-Za-z0-9_:\\]*
    (?:\.[A-Za-z_:\\][A-Za-z0-9_:\\]*|\[[^\]]+\])*
    """,
    re.VERBOSE
)

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def evalMath(path: str) -> int | float:
    def _eval(node) -> int | float:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.UnaryOp):
            return -_eval(node.operand)
        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id.lower()      # normalise to lower case
                match func_name:
                    case "abs":
                        if func_name == "abs":
                            if len(node.args) != 1:
                                raise ValueError("abs() takes exactly one argument")
                            return abs(_eval(node.args[0]))
            raise ValueError(f"Unsupported function call: {ast.dump(node)}")
        raise ValueError("Unsupported math operation")
    tree = ast.parse(path, mode="eval")
    return _eval(tree.body)

def resolveExpr(path: str) -> int | float:
    resolved = path
    for match in PATH_RE.findall(path):
        value = getMemory(match, OutputType.PLC)
        resolved = resolved.replace(match, str(value))
    return evalMath(resolved)

def resolvePath(path: str) -> list[str|int|float]:
    out:list[str] = []
    for part in parsePath(path):
        if isinstance(part, Expr):
            out.append(resolveExpr(part.text))
        else:
            out.append(part)
    return out

def parsePath(s: str|list|tuple) -> list[str|int]:
    if isinstance(s, str):
        tokens = []
        i = 0

        while i < len(s):
            if (s[i].isalpha() or s[i].isdigit()) or s[i] in "_:\\\'":
                start = i
                while i < len(s) and s[i] not in ".[":
                    i += 1
                tokens.append(s[start:i])
            elif s[i] == ".":
                i += 1
            elif s[i] == "[":
                i += 1
                start = i
                depth = 1
                while i < len(s) and depth:
                    if s[i] == "[":
                        depth += 1
                    elif s[i] == "]":
                        depth -= 1
                    i += 1
                tokens.append(Expr(s[start:i-1]))
            else:
                raise SyntaxError(f"Unexpected char {s[i]}")
    else:
        tokens = s
    return tokens

def resolveMathExpr(expr: str) -> str:
    substituted = substituteVariables(expr)
    return evalMath(substituted)

#FUNC_CALL_RE = re.compile(r'([A-Za-z_]\w*)\s*\(([^()]*)$$')
#FUNC_CALL_RE = re.compile(r'(?P<func>[A-Za-z_]\w*)\s*\((?P<arg>[^()]*)\)')

#FUNC_CALL_RE = re.compile(r'(?P<func>[A-Za-z_]\w*)\s*\((?:P<arg>[^()]+|(?R))*)\)')
FUNC_CALL_RE = re.compile(r'(?P<func>[A-Za-z_]\w*)\s*\((?P<arg>(?:[^()]+|(?R))*)\)')



def _apply_function(func_name: str, arg_expr: str) -> int | float:
    resolved_arg = substituteVariables(arg_expr)   # recursion
    numeric_value = evalMath(resolved_arg)

    func_name = func_name.lower()
    match func_name:
        case "abs":
            return abs(numeric_value)
        # Add more functions here if desired
        case _:
            raise ValueError(f"Unsupported function '{func_name}'")

def substituteVariables(expr: str) -> str:
    while True:
        m = FUNC_CALL_RE.search(expr)
        if not m:
            break
        func_name = m.group("func")
        arg_text  = m.group("arg")

        replacement = str(_apply_function(func_name, arg_text))
        expr = expr[:m.start()] + replacement + expr[m.end():]

    result = expr
    for match in PATH_RE.findall(expr):
        value = resolvePathToValue(match)
        result = result.replace(match, str(value))
    return result

def resolvePathToValue(path: str) -> str:
    resolved = []
    for p in parsePath(path):
        if isinstance(p, Expr):
            resolved.append(resolveMathExpr(p.text))
        else:
            resolved.append(p)
    return getMemory(resolved, OutputType.PLC)