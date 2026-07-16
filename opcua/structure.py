import logging
import re

from dataclasses import dataclass, field

def sanitizeName(raw: str, kind: str = 'attr') -> str:
    def _to_pascal(tok: str) -> str:
        parts = [p for p in tok.split('_') if p]
        return ''.join(p.title() for p in parts)

    def _to_snake(tok: str) -> str:
        return re.sub(r'__+', '_', tok)

    raw = raw.upper()
    
    token = raw.lstrip('*')

    token = re.sub(r'[:*]', '_', token)

    if token.startswith('_'):
        token = f'D{token}'

    if re.match(r'^\d', token):
        token = f'D_{token}'

    if kind == 'class':
        return _to_pascal(token)
    else:
        return _to_snake(token)

@dataclass
class StructureField:
    name:str = field(init=True)
    type:int = field(init=True, default=0)
    dataType:str = field(init=True, default=None)
    dimension:list[int] | str = field(init=True, default_factory=lambda : [])

    def __post_init__(self):
        if isinstance(self.dimension, str):
            try:
                dims_list = [int(x) for x in self.dimension.split()]
                if 0 in dims_list:
                    self.dimension = []
                else:
                    self.dimension = dims_list
            except ValueError as e:
                logging.exception(e)
                self.dimension = []
        elif not isinstance(self.dimension, list):
            raise ValueError(f"dimension must be a string or list, got {type(self.dimension)}")
        
        if isinstance(self.dataType, str):
            self.dataType = sanitizeName(self.dataType)

@dataclass
class Structure:
    name:str = field(init=True)
    datavariant:bool = field(init=True, default=False)
    snode:int = field(init=False, default=0)
    nodeid:int = field(init=False, default=0)
    type:int = field(init=False, default=0)
    base:tuple = field(init=False, default_factory=lambda : ())
    fields:list[StructureField] = field(init=False, default_factory=lambda : [])

    def __post_init__(self):
        self.name = sanitizeName(self.name)