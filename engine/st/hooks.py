import types
import asyncio
from typing import Any, Optional

import engine.context
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler

from protocols.memory import SupportsGetPLCValue
from utils.isplcinstance import isPLCInstance

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
    if isPLCInstance(result, SupportsGetPLCValue):
        result = result.getPLCValue()
    return result

def setHook(name, value):
    from core.memory.helper import setMemory
    setMemory(name, value)

def build_exec_env(ctx: "engine.context.ExecutionContext") -> dict:
    from core.registry.instructionregistry import InstructionRegistry
    from engine.instruction import Instruction

    async def callHook(name, args):
        with Hierarchy.scope(name):
            with PLCFaultHandler.minor():
                instance: Instruction = InstructionRegistry.get(name)(name=name, args=args)
                return await instance.st(ctx)

    return {
        "get": getHook,
        "set_": setHook,
        "call": callHook,
    }

async def run_exec_env(expression: str, ctx: "engine.context.ExecutionContext",  error_tag: str, timeout: Optional[float] = 5.0) -> Any:
    exec_env = build_exec_env(ctx)
    
    if not isinstance(expression, types.CodeType):
        expression = make_async_st(expression)

    with PLCFaultHandler.st(error_tag, expression):
        with PLCFaultHandler.minor():
            exec(expression, exec_env)
            
            try:
                return await asyncio.wait_for(exec_env["__st_main__"](), timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"{error_tag}, execution took to long")