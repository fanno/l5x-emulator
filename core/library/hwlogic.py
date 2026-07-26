import logging
import time

from typing import Dict

from simpleeval import simple_eval

from core.memory.memory import Memory
from core.memory.helper import getMemory, setMemory
from datatypes.custom.datavariant import DataVariant

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
        self.runInbound = {}

    def update(self, _name:str, memory:Memory):
        now = time.monotonic()
        if now > self.next_update:
            self.next_update = now + (self.update_ms / 1000 )

            outputs = {}
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

            eval_func = create_evaluator(_name, eval_context)

            for out_name, expression in self.runOutbound[self.outAddress].items():
                result = eval_func(expression)
                eval_context[out_name] = result

            if self.updateInbound:
                for item in self.runInbound[self.inAddress]:
                    if isinstance(item, str):
                        eval_func(item)

                    elif isinstance(item, dict):
                        condition = eval_func(item["if"])

                        branch = item["then"] if condition else item.get("else", [])

                        for expr in branch:
                            eval_func(expr)
            self.updateInbound = not self.updateInbound

            return outputs

def create_evaluator(name, namespace):

    def get_value(path_str):
        return getMemory(f"{name}:{path_str}")
    
    def set_value(path_str, value):
        setMemory(f"{name}:{path_str}", value)

    def get_bits(path_str, start, length):
        if isinstance(path_str, str):
            value = getMemory(f"{name}:{path_str}")

            if isinstance(value, DataVariant):
                value.getPLCValue()
        else:
            value = path_str

        mask = (1 << length) - 1
        return (value >> start) & mask

    def evaluate(expression):
        try:
            result = simple_eval(
                expression,
                names=namespace,
                functions={'get': get_value, 'set': set_value, 'get_bits': get_bits}
            )
            return result
        except Exception as e:
            logging.exception(e)
            return None

    return evaluate
