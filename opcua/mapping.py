from typing import Optional

from core.signal import Signal
from utils.biindexmap import BiIndexMap

class Mapping(BiIndexMap[Signal]):
    def __init__(self):
        super().__init__(
            key1_func=lambda s: s.PATH,
            key2_func=lambda s: s.NODE.nodeid.Identifier,
            expected_type=Signal 
        )

    def getByPath(self, path: str) -> Optional["Signal"]:
        return self._get_by_first(path)

    def getById(self, id: str) -> Optional["Signal"]:
        return self._get_by_second(id)