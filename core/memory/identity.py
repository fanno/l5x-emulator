from dataclasses import dataclass

@dataclass
class Identity:
    def __hash__(self):
        return id(self)