from __future__ import annotations

import engine.context
from engine.instruction import Instruction

from engine.errors import MinorException
from core.emulatorfault import EmulatorFault

def parse(text:str) -> Series:
    tokens = tokenize(text)
    tree, _ = series(tokens)
    return tree

def tokenize(text:str) -> list[str]:
    tokens:list[str] = []
    buf = ""

    paren_depth = 0

    for c in text:
        if c == "(":
            paren_depth += 1
            buf += c
            continue

        if c == ")":
            paren_depth -= 1
            buf += c
            continue

        if paren_depth == 0 and c in ["[", "]", ","]:
            if buf.strip():
                tokens.append(buf.strip())
                buf = ""
                
            tokens.append(c)
        else:
            buf += c

    if buf.strip():
        tokens.append(buf.strip())

    return tokens

def parallel(tokens, idx):
    branches = []

    while True:
        branch, idx = series(tokens, idx)
        branches.append(branch)

        if tokens[idx] == ",":
            idx += 1
            continue

        if tokens[idx] == "]":
            idx += 1
            break

    return Parallel(branches), idx

def split_instructions(tok:str) -> list[str]:
    parts:list[str] = []
    depth = 0
    start = 0

    for i, ch in enumerate(tok):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1

            if depth == 0:
                j = i + 1
                while j < len(tok) and tok[j].isspace():
                    j += 1

                if j < len(tok) and tok[j].isupper():
                    parts.append(tok[start:i+1])
                    start = j

    parts.append(tok[start:])
    return parts

def series(tokens, idx=0):
    nodes:list[InstructionNode] = []

    while idx < len(tokens):
        tok = tokens[idx]
        
        if tok == "[":
            node, idx = parallel(tokens, idx + 1)
            nodes.append(node)
            continue

        if tok in ["]", ","]:
            break
        
        tok = split_instructions(tok)

        for t in tok:
            nodes.append(InstructionNode(t))
        idx += 1

    return Series(nodes), idx

def instruction(token):
    name, rest = token.split("(", 1)

    rest = rest.strip()
    if rest.endswith(")"):
        rest = rest[:-1]


    args = [arg.strip() for arg in rest.split(",") if arg.strip()]

    return name.strip(), args
'''
class Node:
    nodes:list[Node]

    def eval(self, ctx) -> None:
        raise NotImplementedError(f"Unsupported operator: {self}")

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(map(str, self.nodes))})"
'''

class InstructionNode:
    nodes:list[InstructionNode]
    name = ""
    args = []
    instance:Instruction = None

    def __init__(self, token):
        from core.registry.instructionregistry import InstructionRegistry
        
        self.name, self.args = instruction(token)
        cls = InstructionRegistry.get(self.name)

        self.instance = cls(self.name, self.args)

    async def eval(self, ctx:"engine.context.ExecutionContext") -> None:
        try:
            await self.instance.execute(ctx)
        except MinorException as e:
            EmulatorFault.prepend(e)

    def __str__(self):
        return f"{self.name}{self.args}"
    
    def getLabel(self):
        if self.nodes:
            if len(self.nodes) > 1:
                first_element = self.nodes[0]
                if first_element.name == "LBL":
                    return first_element.args[0]
        return None

class Parallel(InstructionNode):

    def __init__(self, branches:list[InstructionNode]):
        self.nodes = branches

    async def eval(self, ctx:"engine.context.ExecutionContext") -> None:
        input_power = ctx.RungStatus
        input_enable = ctx.RungEnabled
        output_power = False
        output_enable = False

        for node in self.nodes:
            ctx.RungEnabled = input_enable
            ctx.RungStatus = input_power
            if ctx.RungEnabled:
                await node.eval(ctx)
            else:
                ctx.RungStatus = False
            output_power |= ctx.RungStatus
            output_enable |= ctx.RungEnabled

            if ctx.Jump is not None:
                break

        ctx.RungStatus = output_power
        ctx.RungEnabled = output_enable

class Series(InstructionNode):
    def __init__(self, series:list[InstructionNode]):
        self.nodes = series
        
    async def eval(self, ctx:"engine.context.ExecutionContext") -> None:
        for node in self.nodes:
            if ctx.RungEnabled:
                await node.eval(ctx)
            if ctx.Jump is not None:
                break