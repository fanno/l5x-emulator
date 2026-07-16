import yaml
import logging
from typing import Dict

from simpleeval import simple_eval

from core.memory.memory import Memory
from core.memory.helper import getMemory, setMemory

class HWLogic:
    def __init__(self, yaml_data):
        self.id = yaml_data.get('id', "")
        self.vendor = yaml_data.get('vendor', "")

        self.outbound = yaml_data.get('outbound', {})

        self.inbound = yaml_data.get('inbound', {})
        

        self.constants = yaml_data.get('constants', {})
        
        self.inType = None
        self.inAddress = None
        self.outType = None
        self.outAddress = None

        self.runOutbound = {}
        self.runInbound = {}
        logging.debug(yaml_data)

    def update(self, _name:str, memory:Memory):
        outputs = {}

        if not self.runOutbound:
            _out = memory.get(f"{_name}:O")

            if _out:
                _, n = _out.__class__.__name__.split(f"{self.id}_")
                self.outType, _, self.outAddress = n.split("_")

                logging.debug(f"id: {self.id}, {self.outType} {self.outAddress}")

                self.runOutbound = self.outbound[self.outType]

        if not self.runInbound:
            _in = memory.get(f"{_name}:I")
            if _in:
                _, n = _in.__class__.__name__.split(f"{self.id}_")
                self.inType, _, self.inAddress = n.split("_")
                logging.debug(f"id: {self.id}, {self.inType} {self.inAddress}")
                self.runInbound = self.inbound[self.inType]

        eval_context = {**self.constants}
        eval_func = create_evaluator(_name, eval_context)

        for out_name, expression in self.runOutbound[self.outAddress].items():
            result = eval_func(expression)
            eval_context[out_name] = result

        for expression in self.runInbound[self.inAddress]:
            logging.debug(f"expression: {expression}")
            result = eval_func(expression)

        return outputs

def create_evaluator(name, namespace):

    def get_value(path_str):
        logging.debug(f"get_value: {name}:{path_str}")
        return getMemory(f"{name}:{path_str}")
    
    def set_value(path_str, value):
        logging.debug(f"get_value: {name}:{path_str}:{value}")
        setMemory(f"{name}:{path_str}", value)

    def evaluate(expression):
        try:
            result = simple_eval(
                expression,
                names=namespace,
                functions={'get': get_value, 'set': set_value}
            )
            return result
        except Exception as e:
            logging.exception(e)
            return None

    return evaluate
