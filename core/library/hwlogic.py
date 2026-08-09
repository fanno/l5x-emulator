import logging
import time

from typing import Dict

from ast import Expr

from simpleeval import SimpleEval

from core.memory.memory import Memory
from core.memory.helper import getMemory, setMemory

from protocols.memory import SupportsGetPLCValue
from utils.isplcinstance import isPLCInstance

class HWLogic:
    def __init__(self, yaml_data:Dict):

        self.id = yaml_data.get('id', "")
        self.vendor = yaml_data.get('vendor', "")
        self.update_ms = yaml_data.get('update_ms', 1000)
        self.outbound = yaml_data.get('outbound', {})
        self.inbound = yaml_data.get('inbound', {})
        self.constants = yaml_data.get('constants', {})
        
        self.inType = None
        self.inAddress = None
        self.outType = None
        self.outAddress = None

        self.next_update = 0
        self.updateInbound = False

        self.runOutbound = {}
        self.compinedOutbound = {}
        self.runInbound = {}
        self.compinedInbound = {}

    def update(self, _name:str, memory:Memory):
        now = time.monotonic()
        if now > self.next_update:
            self.next_update = now + (self.update_ms / 1000 )

            if not self.runOutbound:
                _out = memory.get(f"{_name}:O")

                if _out:
                    _, n = _out.__class__.__name__.split(f"{self.id}_")
                    self.outType, _, self.outAddress = n.split("_")
                    self.runOutbound = self.outbound[self.outType]

            if not self.runInbound:
                _in = memory.get(f"{_name}:I")
                if _in:
                    _, n = _in.__class__.__name__.split(f"{self.id}_")
                    self.inType, _, self.inAddress = n.split("_")
                    self.runInbound = self.inbound[self.inType]

            eval_context = {**self.constants}

            eval__compined_func = create_evaluator(_name, eval_context)

            if self.outAddress not in self.compinedOutbound:
                self.compinedOutbound[self.outAddress] = {}
                for out_name, expression in self.runOutbound[self.outAddress].items():
                    self.compinedOutbound[self.outAddress][out_name] = compile_item(expression)

            for out_name, expression in self.compinedOutbound[self.outAddress].items():
                result = eval__compined_func(expression)
                if result is not None:
                    eval_context[out_name] = result

            if self.updateInbound:
                if self.inAddress not in self.compinedInbound:
                    self.compinedInbound[self.inAddress] = []
                    for item in self.runInbound[self.inAddress]:
                        self.compinedInbound[self.inAddress].append(compile_item(item))

                for item in self.compinedInbound[self.inAddress]:
                    if isinstance(item, Expr):
                        eval__compined_func(item)
                    elif isinstance(item, dict):
                        condition = eval__compined_func(item["if"])

                        branch = item["then"] if condition else item.get("else", [])

                        for expr in branch:
                            eval__compined_func(expr)
                         
            self.updateInbound = not self.updateInbound

def compile_item(item):
    try:
        if isinstance(item, str):
            return SimpleEval.parse(item)
        
        return {
            "if": SimpleEval.parse(item["if"]),
            "then": [compile_item(x) for x in item.get("then", [])],
            "else": [compile_item(x) for x in item.get("else", [])]
        }
    except Exception as e:
        logging.exception(e)
    return None

def create_evaluator(name, namespace):

    def get_value(path_str):
        return getMemory(f"{name}:{path_str}")
    
    def set_value(path_str, value):
        setMemory(f"{name}:{path_str}", value)

    def get_bits(path_str, start, length):
        if isinstance(path_str, str):
            value = getMemory(f"{name}:{path_str}")

            if isPLCInstance(value, SupportsGetPLCValue):
                value.getPLCValue()
        else:
            value = path_str

        mask = (1 << length) - 1
        return (value >> start) & mask

    def evaluate(expression):
        if isinstance(expression, Expr):
            try:
                s = SimpleEval()
                s.names = namespace
                s.functions = {
                    'get': get_value,
                    'set': set_value,
                    'get_bits': get_bits
                }
                result = s._eval(expression)

                return result
            except Exception as e:
                logging.exception(e)
        return None
    return evaluate