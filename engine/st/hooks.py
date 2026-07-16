from datatypes.custom.datavariant import DataVariant

def make_async_st(st_source: str) -> str:
    indented = indent(st_source, "    ")
    if not indented.strip():
        indented = "    pass"
    return "async def __st_main__():\n" + indented + "\n"

def indent(code: str, prefix: str) -> str:
    return "\n".join(
        prefix + line if line.strip() else line
        for line in code.splitlines()
    )

def getHook(name):
    from core.memory.helper import getMemory
    result = getMemory(name)
    if isinstance(result, DataVariant):
        result = result.getPLCValue()
    return result

def setHook(name, value):
    from core.memory.helper import setMemory

    setMemory(name, value)