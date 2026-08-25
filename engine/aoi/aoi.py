from typing import TypeVar, Dict, ClassVar, Any, Optional, Dict, TYPE_CHECKING
from contextlib import contextmanager
from lxml.etree import _Element as Element
from dataclasses import dataclass, field, InitVar, fields

from core.objectregistry import ObjectRegistry
from core.registry.datatyperegistry import DataTypeRegistry

if TYPE_CHECKING:
    from engine.context import ExecutionContext
    from engine.routine import Routine
from engine.instruction import Instruction
from engine.hierarchy import Hierarchy
from engine.errors import PLCFaultHandler
from engine.scan import PreScan, PostScan
from engine.aoi.memory import AOIMemory
from engine.context import EmulatorContext

from datatypes.custom.bool import BOOL
from datatypes.custom.dt import DT
from datatypes.custom.numbers import LINT, DINT
from datatypes.custom.string import STRING
from datatypes.custom.array import Array

from protocols.memory import HasEnable

TT = TypeVar("TT", bound=type)

@dataclass
class Parameter():
    Usage:str = field(init=True)
    DataType:str = field(init=True)
    Name:str = field(init=True)
    Required:bool = field(init=True)

    def __post_init__(self):
        if isinstance(self.Required , str):
            self.Required = BOOL.toValue(self.Required)

@dataclass
class Local():
    element: InitVar[Element]

    Name:str = field(init=False)
    DataType:str = field(init=False)
    Dimensions:int = field(init=False)

    def __post_init__(self, element:Element):
        if isinstance(element, Element):
            self.Name = element.get("Name")
            self.DataType = element.get("DataType")
            self.Dimensions = int(element.get("Dimensions", "0"))

    def getVariable(self) -> Any:
        cls = DataTypeRegistry.get(self.DataType)
        if self.Dimensions == 0:
            return cls()
        else:
            return Array[cls](cls, [cls()] * self.Dimensions)

@dataclass
class AOI():
    element: InitVar[Element]

    Routines: Dict[str, "Routine"] = field(init=False, default_factory=lambda: {})
    Name:str = field(init=False)
    Parameters: list[Parameter] = field(init=False, default_factory=lambda: [])
    Locals: list[Local] = field(init=False, default_factory=lambda: [])
    LastEditDate:LINT = field(init=False, default_factory=LINT)
    MajorRevision:DINT = field(init=False, default_factory=DINT)
    MinorRevision:DINT = field(init=False, default_factory=DINT)
    RevisionExtendedText:STRING = field(init=False, default_factory=STRING)
    SafetySignatureID:DINT = field(init=False, default_factory=DINT)
    SignatureID:DINT = field(init=False, default_factory=DINT)
    Vendor:DINT = field(init=False, default_factory=DINT)
    ExecutePrescan:BOOL = field(init=False, default_factory=BOOL)
    ExecutePostscan:BOOL = field(init=False, default_factory=BOOL)
    ExecuteEnableInFalse:BOOL = field(init=False, default_factory=BOOL)

    def __post_init__(self, element:Element):
        from engine.routine import Routine
        
        self.Name = element.get("Name")

        dt = DT(element.get("EditedDate"))
        self.LastEditDate:LINT = LINT(dt.getPLCValue())

        Revision = element.get("Revision").split('.')
        self.MajorRevision.setValue(Revision[0])
        self.MinorRevision.setValue(Revision[1])

        self.ExecutePrescan = BOOL(element.get("ExecutePrescan", False))
        self.ExecutePostscan = BOOL(element.get("ExecutePostscan", False))
        self.ExecuteEnableInFalse = BOOL(element.get("ExecuteEnableInFalse", False))

        for element in element.findall("./LocalTags//LocalTag"):
            p = Local(element=element)
            self.Locals.append(p)

        for parameter in element.findall("./Parameters//Parameter"):
            p = Parameter(Usage=parameter.get('Usage'),
                          DataType=parameter.get('DataType'),
                          Name=parameter.get('Name'),
                          Required=parameter.get('Required'),)
            self.Parameters.append(p)

        for routine in element.findall("./Routines//Routine"):
            r = Routine(routine)
            self.Routines[r.Name] = r

    async def execute(self, args:list[str], ctx:"ExecutionContext"):
        with Hierarchy.scope(self.Name):
            with PLCFaultHandler.minor():
                from engine.context import ExecutionContext
                context = ExecutionContext(ProgramRef=self)

                emulator = EmulatorContext.get()
                context.RungStatus = ctx.RLL.RungStatus

                if emulator.preScan:
                    if self.ExecutePrescan:
                        if "Prescan" in self.Routines:
                            with PreScan.scope(emulator):
                                await self.Routines["Prescan"].execute(context)
                elif emulator.preScan:
                    if self.ExecutePostscan:
                        if "Postscan" in self.Routines:
                            with PostScan.scope(emulator):
                                await self.Routines["Postscan"].execute(context)
                elif not context.RungStatus:
                    if self.ExecuteEnableInFalse:
                        if "EnableInFalse" in self.Routines:
                            await self.Routines["EnableInFalse"].execute(context)
                else:
                    if "Logic" in self.Routines:
                        await self.Routines["Logic"].execute(context)

class AOIRegistry:
    _registry: ClassVar[Dict[str, AOI]] = {}
    _cache: ClassVar[Dict[str, Any]] = {}

    @staticmethod
    def register(cls: AOI) -> None:
        AOIRegistry._registry[cls.Name] = cls

    @staticmethod
    def has(name:str) -> bool:
        return name in AOIRegistry._registry
    
    @staticmethod
    def get(name:str) -> AOI:
        return AOIRegistry._registry[name]
    
    @staticmethod
    def clear() -> None:
        AOIRegistry._registry = {}
        AOIRegistry._cache = {}

    @staticmethod
    def registerCache(key:str, cls: Instruction) -> None:
        AOIRegistry._cache[key] = cls

    @staticmethod
    def hasCache(key:str) -> bool:
        return key in AOIRegistry._cache
    
    @staticmethod
    def getCache(key:str) -> Instruction:
        return AOIRegistry._cache[key]

class AOI_CLASS(Instruction):
    aoiObject:AOI
    aoiName:str

    def __init__(self, name:str, args:list[str]):
        super().__init__(name, args)
        self.aoiName = self.args[0]
        self.args = self.args[1:]

        self.aoiObject = AOIRegistry.get(self.name)

    async def execute(self, ctx:"ExecutionContext") -> None:
        with Hierarchy.scope(self.aoiName):
            with PLCFaultHandler.minor():
                from core.memory.helper import getMemory, setMemory
                try:
                    aoiData = getMemory(self.aoiName)

                    if isinstance(aoiData, HasEnable):
                        aoiData.EnableIn.setValue(ctx.RLL.RungStatus)
                    else:
                        raise TypeError("Returned AOI does not implement EnableIn/EnableOut")

                    from engine.aoi.memory import AOIMemory
                    aoi = ObjectRegistry.get(aoiData, AOIMemory)

                    if aoi.memory.size() == 0:
                        for field in fields(aoiData):
                            if field.repr:
                                aoi.memory.set(field.name, getattr(aoiData, field.name))

                    i = 0
                    for p in self.aoiObject.Parameters:
                        if p.Required or p.Usage == 'InOut':
                            value = getMemory(self.args[i])
                            aoi.memory.set(p.Name, value)
                            i += 1
                    with AOIContextMemory.scope(aoi):
                        await self.aoiObject.execute(self.args, ctx)

                    ctx.RLL.RungStatus = aoiData.EnableOut.getPLCValue()
                except Exception as e:
                    raise e
                finally:
                    i = 0
                    for p in self.aoiObject.Parameters:
                        if p.Required or p.Usage == 'InOut':
                            if p.Usage != 'Input':
                                value = aoi.memory.get(p.Name)
                                setMemory(self.args[i], value)
                            i += 1
                        if p.Usage == 'Output':
                            value = aoi.memory.get(p.Name)
                            setattr(aoiData, p.Name, value)

    async def ladder(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def fbd(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def st(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def sfc(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

class AOIContextMemory:
    _stack: list[AOIMemory] = []
    
    @classmethod
    @contextmanager
    def scope(cls, ctx:AOIMemory):

        cls._stack.append(ctx)
        try:
            yield
        finally:
            cls._stack.pop()

    @classmethod
    def get(cls) -> Optional[AOIMemory]:
        return cls._stack[-1] if cls._stack else None