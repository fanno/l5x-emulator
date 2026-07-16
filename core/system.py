from asyncua import Server

from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:    
    from core.memory.memory import Memory
from core.xml.tags import createTagsMemory
from core.constants import SYSTEMTAGS

from opcua.tag import OpcuaTag, Tag
from opcua.mapping import Mapping
from opcua.helpers import createVariant

from engine.plcclock import PLCClock

@dataclass
class System():
    _instance: "System | None" = None 

    server:Server = field(init=False)
    NAME:str = field(init=False, default=SYSTEMTAGS)

    memory:"Memory" = field(init=False)
    mapping:Mapping = field(init=False, default_factory=Mapping)
    opcua:OpcuaTag = field(init=False)

    clock:PLCClock = field(init=False, default_factory=PLCClock)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __post_init__(self):
        from core.memory.memory import Memory, PlcMemory

        self.memory = Memory(NAME=self.NAME)
        PlcMemory.addContainer(self.memory)

    async def init(self, server:Server):
        self.server = server

        self.opcua = OpcuaTag(NAME=self.NAME,
                              SERVER=self.server)
        await self.opcua.registerNamespace("http://rockwell.plc")
        await self.opcua.createFolder(self.NAME)

        await self.loadSystemTags()
        await createTagsMemory(self.opcua, self.memory, self.mapping)

    async def loadSystemTags(self):
        await self._createSystemTag("S:FS", initialValue="1")
        await self._createSystemTag("S:N")
        await self._createSystemTag("S:Z")
        await self._createSystemTag("S:V")
        await self._createSystemTag("S:MINOR")

    async def _createSystemTag(self, name:str, dataType:str="BOOL", initialValue:str="0"):
        t = Tag(Name=name, DataType=dataType, Dimensions=[])
        t.Variant = createVariant(initialValue, t.DataType)

        self.opcua.tags[t.Name] = t

PLCSYSTEM:System = System()