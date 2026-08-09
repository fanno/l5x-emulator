from typing import Optional

from core.signal import Signal
from utils.indexmap import IndexMap

from protocols.memory import SupportsSetValue
from utils.isplcinstance import isPLCInstance

class Mapping(IndexMap[Signal]):

    def __init__(self):
        super().__init__(expected_type=Signal)

        self.IDX_PATH = self._addIndex(lambda s: s.PATH)
        self.IDX_NODE = self._addIndex(lambda s: s.NODE.nodeid.Identifier)
        self.IDX_MEMORY = self._addIndex(lambda s: id(s.MEMORY) if isPLCInstance(s.MEMORY, SupportsSetValue) else None)

    def getByPath(self, path: str | list | tuple ) -> Optional["Signal"]:

        return self.get(self.IDX_PATH, path)

    def getById(self, id: str) -> Optional["Signal"]:
        return self.get(self.IDX_NODE, id)

    def getByMemoryObject(self, obj ) -> Optional["Signal"]:
        return self.get(self.IDX_MEMORY, id(obj))