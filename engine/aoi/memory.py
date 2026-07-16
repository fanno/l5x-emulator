from dataclasses import dataclass, field

from core.memory.memory import Memory
from core.memory.identity import Identity

@dataclass
class AOIMemory(Identity):
    memory:Memory = field(init=False, default_factory=lambda: Memory(NAME="local"))