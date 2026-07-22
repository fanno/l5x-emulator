from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from typing import TypeVar, Dict, ClassVar, Any, Protocol, runtime_checkable, Optional, Dict, TYPE_CHECKING

from core.objectregistry import ObjectRegistry
from core.registry.datatyperegistry import DataTypeRegistry

if TYPE_CHECKING:
    from engine.context import ExecutionContext
    from engine.routine import Routine
    
from engine.instruction import Instruction
from engine.errors import AOIException

from datatypes.custom.bool import BOOL
from datatypes.custom.dt import DT
from datatypes.custom.numbers import LINT, DINT
from datatypes.custom.string import STRING
from datatypes.custom.array import Array

TT = TypeVar("TT", bound=type)

@dataclass
class Parameter():
    Usage:str = field(init=True)
    DataType:str = field(init=True)
    Name:str = field(init=True)
    Required:bool = field(init=True)

    def __post_init__(self):
        if isinstance(self.Required , str):
            self.Required = self.Required == 'true'

@dataclass
class Local():
    _Element: Element = field(init=True)

    Name:str = field(init=False)
    DataType:str = field(init=False)
    Dimensions:int = field(init=False)

    def __post_init__(self):
        self.Name = self._Element.get("Name")
        self.DataType = self._Element.get("DataType")
        self.Dimensions = int(self._Element.get("Dimensions", "0"))

    def getVariable(self) -> Any:
        cls = DataTypeRegistry.get(self.DataType)
        if self.Dimensions == 0:
            return cls()
        else:
            return Array[cls](cls, [cls()] * self.Dimensions)

@runtime_checkable
class HasEnable(Protocol):
    EnableIn:BOOL
    EnableOut:BOOL

@dataclass
class AOI():
    _Element: Element = field(init=True)
    Routines: Dict[str, "Routine"] = field(init=False, default_factory=lambda: {})
    MainRoutineName: Optional[str] = field(init=False, default="Logic")
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

    def __post_init__(self):
        from engine.routine import Routine
        
        self.Name = self._Element.get("Name")

        dt = DT(self._Element.get("EditedDate"))
        self.LastEditDate:LINT = LINT(dt.getPLCValue())

        Revision = self._Element.get("Revision").split('.')
        self.MajorRevision.setValue(Revision[0])
        self.MinorRevision.setValue(Revision[1])

        for element in self._Element.findall("./LocalTags//LocalTag"):
            p = Local(_Element=element)
            self.Locals.append(p)

        for parameter in self._Element.findall("./Parameters//Parameter"):
            p = Parameter(Usage=parameter.get('Usage'),
                          DataType=parameter.get('DataType'),
                          Name=parameter.get('Name'),
                          Required=parameter.get('Required'),)
            self.Parameters.append(p)

        for routine in self._Element.findall("./Routines//Routine"):
            r = Routine(routine)
            self.Routines[r.Name] = r

    async def execute(self, args:list[str], ctx:"ExecutionContext"):
        from engine.context import ExecutionContext
        context = ExecutionContext(ProgramRef=self)
        await self.Routines[self.MainRoutineName].execute(context)

class AOIRegistry:
    _registry: ClassVar[Dict[str, AOI]] = {}

    @staticmethod
    def register(cls: AOI) -> None:
        if cls.Name in AOIRegistry._registry:
            raise ValueError(f"AOI {cls.Name} already registered")
        AOIRegistry._registry[cls.Name] = cls

    @staticmethod
    async def execute(name:str, args:list[str], ctx:"ExecutionContext") -> None:
        from engine.context import ExecutionContext
        if name not in AOIRegistry._registry:
            raise KeyError(f"AOI {name} not supported")
        
        from engine.helper import _pushAOIMemory, _popAOIMemory
        from core.memory.helper import getMemory, setMemory
        token = None
        try:
            instance = args[0]
            rest = args[1:]

            aoiObject = AOIRegistry._registry[name]

            aoiData = getMemory(instance)

            if isinstance(aoiData, HasEnable):
                aoiData.EnableIn.setValue(ctx.RungEnabled)
            else:
                raise TypeError("Returned AOI does not implement EnableIn/EnableOut")

            from engine.aoi.memory import AOIMemory
            aoi = ObjectRegistry.get(aoiData, AOIMemory)

            if aoi.memory.size() == 0:
                for local in aoiObject.Locals:
                    aoi.memory.set(local.Name, local.getVariable())

            for attr, value in aoiData.__dict__.items():
                aoi.memory.set(attr, value)

            i = 0
            for p in aoiObject.Parameters:
                if p.Required or p.Usage == 'InOut':
                    value = getMemory(rest[i])
                    
                    aoi.memory.set(p.Name, value)
                    i += 1

            token = _pushAOIMemory(aoi)
            await aoiObject.execute(args, ctx)
        except Exception as e:
            raise AOIException(name, instance).with_traceback(e.__traceback__)
        finally:
            if token:
                _popAOIMemory(token)

                i = 0
                for p in aoiObject.Parameters:
                    if p.Required or p.Usage == 'InOut':
                        if p.Usage != 'Input':
                            value = aoi.memory.get(p.Name)
                            setMemory(rest[i], value)
                        i += 1
                    if p.Usage == 'Output':
                        value = aoi.memory.get(p.Name)
                        setattr(aoiData, p.Name, value)

    @staticmethod
    def has(name:str) -> bool:
        return name in AOIRegistry._registry
    
    @staticmethod
    def get(name:str) -> AOI:
        return AOIRegistry._registry[name]

class AOI_CLASS(Instruction):
    aoiObject:AOI
    aoiName:str

    def __init__(self, name:str, args:list[str]):
        super().__init__(name, args)

        self.aoiName = self.args[0]
        self.args = self.args[1:]

        self.aoiObject = AOIRegistry._registry[self.name]

    async def execute(self, ctx:"ExecutionContext") -> None:
        from engine.context import ExecutionContext
        from engine.helper import _pushAOIMemory, _popAOIMemory
        from core.memory.helper import getMemory, setMemory
        token = None
        try:
            aoiData = getMemory(self.aoiName)

            if isinstance(aoiData, HasEnable):
                aoiData.EnableIn.setValue(ctx.RungEnabled)
            else:
                raise TypeError("Returned AOI does not implement EnableIn/EnableOut")

            from engine.aoi.memory import AOIMemory
            aoi = ObjectRegistry.get(aoiData, AOIMemory)

            if aoi.memory.size() == 0:
                for local in self.aoiObject.Locals:
                    aoi.memory.set(local.Name, local.getVariable())

            for attr, value in aoiData.__dict__.items():
                aoi.memory.set(attr, value)

            i = 0
            for p in self.aoiObject.Parameters:
                if p.Required or p.Usage == 'InOut':
                    value = getMemory(self.args[i])
                    
                    aoi.memory.set(p.Name, value)
                    i += 1

            token = _pushAOIMemory(aoi)
            await self.aoiObject.execute(self.args, ctx)
        except Exception as e:
            raise e
        finally:
            if token:
                _popAOIMemory(token)
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

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def ladder_preScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)
    
    async def ladder_postScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def fbd_execute(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def fbd_preScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)
    
    async def fbd_postScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def sfc_execute(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)
    
    async def sfc_preScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)
    
    async def sfc_postScan(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        await self.execute(ctx)