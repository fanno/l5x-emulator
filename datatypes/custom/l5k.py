from dataclasses import dataclass

from core.l5k.l5kreader import L5KReader

@dataclass
class L5K:

    def fromL5K(self, data:L5KReader|str|list) -> L5KReader:
         raise NotImplementedError(f"{__class__.__name__} fromL5K not implemented yet")

    @classmethod
    def getReader(cls, data:L5KReader|str|list|None):
        if isinstance(data, L5KReader):
            return data

        return L5KReader(data)
