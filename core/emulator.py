import logging
import copy
import asyncio
import threading
import time

import instructions
import datatypes
import modules

from queue import Queue

from typing import Dict, Union
from xml.etree.ElementTree import Element, parse
from queue import Empty
from asyncua.common.callback import CallbackType, ServerItemCallback, CallbackService
from asyncua import Server
from asyncua.ua import WriteParameters

from core.datatypes import get_ua_info, DataTypes
from core.registry.datatyperegistry import DataTypeRegistry
from core.memory.memory import Memory, PlcMemory
from core.memory.safetymap import SafetyMap
from core.events import LogEvent, StatusEvent, UpdateVariableEvent
T = Union[StatusEvent, UpdateVariableEvent]

from eventbus.eventbus import EventBus, EventListener, subscribe_event

from core.system import PLCSYSTEM
from core.constants import CONTROLLERTAGS
from core.signal import updateSignal, updateMemory
from core.xml.models import loadModules
from core.xml.tags import loadTags
from core.xml.datatypes import loadDataTypes
from core.xml.programs import loadPrograms
from core.xml.aoi import loadAoiDefinition
from core.xml.task import loadTasks
from core.servicelocator import ServiceLocator
from core.emulatorfault import EmulatorFault
from core.library.libeary import initialize_custom_folder, load_all_hardware, get_paths
from core.library.hwlogic import HWLogic
from core.log import IndentedFormatter
from core.emulatorcontext import EmulatorContext
from opcua.structure import Structure, StructureField
from opcua.tag import OpcuaTag
from opcua.mapping import Mapping
from engine.program import Program
from engine.task import Task
from engine.errors import MajorFault

from datatypes.custom.module import MODULE
from datatypes.custom.string import STRING

class EmulatorLogHandler(logging.Handler):
    def __init__(self, level = 0):
        super().__init__(level)

    def emit(self, record):
        try:
            EventBus.get().dispatch(LogEvent(self.format(record), record.levelname))
        except Exception:
            pass

class Emulator(EventListener, threading.Thread):
    PATH:str
    NAME:str

    programs:Dict[str, Program]
    tasks:Dict[str, Task]
    modules:Dict[str, MODULE]
    modulesLogic:Dict[str, HWLogic]

    memory:Memory
    mapping:Mapping
    root:Element
    controller:Element

    queue:Queue[T]

    _server:Server
    _loop:asyncio.AbstractEventLoop
    _endpoint:str
    _throttle:int

    ProcessorType:STRING
    DeviceName:STRING

    ServiceName:STRING = 'Emulator'
    safetyMap:SafetyMap

    context:EmulatorContext
    
    def __init__(self, path:str, port:int=4840):
        super().__init__()
        self.context = EmulatorContext(True)

        initialize_custom_folder()

        self.queue = Queue()

        self.programs = {}
        self.tasks = {}
        self.modules = {}
        self.modulesLogic = {}
        self.mapping = Mapping()
        self._server = Server()
        self.safetyMap = SafetyMap()
        self.preScan = True

        self._loop = None
        self._throttle = 4

        gui_handler = EmulatorLogHandler(logging.ERROR)

        gui_handler.setFormatter(IndentedFormatter(
            "[%(asctime)s, %(filename)s:%(lineno)s - %(funcName)s()] %(levelname)s \n"
            "%(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        ))

        logging.getLogger().addHandler(gui_handler)

        self.daemon = False
        self.running = False
        self.loop = None

        self._endpoint = f"opc.tcp://127.0.0.1:{port}/plc"
        self.NAME = CONTROLLERTAGS
        self.PATH = path

        EventBus.get().dispatch(StatusEvent(EndPoint=self._endpoint))

        self.root = parse(self.PATH).getroot()
        self.controller = self.root.find("./Controller")

        self.setParameters()

        self.memory = Memory(NAME=self.NAME)
        PlcMemory.addContainer(self.memory)

    def __post_init__(self):
        pass

    def setParameters(self):
        self.ProcessorType = STRING(self.controller.get("ProcessorType", ""))
        self.DeviceName = STRING(self.controller.get("Name", ""))

    def run(self):
        ServiceLocator.register(self)

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._main())
        except Exception as e:
            logging.exception("An error occurred, in the server thread")
        finally:
            pass

    async def _main(self):
        self._is_running = True
        await self.init()

        await self._server.start()

        logging.info("Application started")
        logging.info(f"Server running at: {self._endpoint}")
        difTimeMax:float = 0.0
        lastDrawUi:float = 0.0
        scanCount:int = 0

        while self._is_running:
            try:
                if not EmulatorFault.hasMajorFault():
                    startTime = time.monotonic()
                    await self.mainloop()
                    scanCount += 1
                    endTime = time.monotonic()
                    difTime = endTime - startTime

                    if (difTime > difTimeMax):
                        difTimeMax = difTime

                    scanDelayTime = difTimeMax * self._throttle
                    if lastDrawUi < startTime:
                        data = {}

                        data[PLCSYSTEM.NAME] = copy.deepcopy(PLCSYSTEM.memory.getMemoryAll())
                        data[self.NAME] = copy.deepcopy(self.memory.getMemoryAll())
                        for pname, program in self.programs.items():
                            data[program.Name] = copy.deepcopy(program.memory.getMemoryAll())

                        EventBus.get().dispatch(StatusEvent(Runing=True,
                                                ScanCurrent=difTime,
                                                ScanDelayed=scanDelayTime,
                                                ScanMax=difTimeMax,
                                                ControllerName=self.DeviceName.getPLCValue(),
                                                ControllerType=self.ProcessorType.getPLCValue(),
                                                EndPoint=self._endpoint,
                                                ScanCount=scanCount,
                                                Tags=data))

                        lastDrawUi = startTime + 1

                    if difTime < scanDelayTime:
                        await asyncio.sleep(scanDelayTime-difTime)
            except MajorFault as e:
                EmulatorFault.setMajorFault(e)
            except Exception as e:
                logging.exception(e)
                break

    async def init(self):
        self._server.set_endpoint(self._endpoint)
        self._server.set_server_name("RockwellEmulator")
        await self._server.init()
        self._server.subscribe_server_callback(CallbackType.PostWrite, self.CallbackTypePostWrite)

        self.opcua = OpcuaTag(NAME=self.NAME,
                              SERVER=self._server)
        await self.opcua.registerNamespace("http://rockwell.plc")
        await self.opcua.createFolder(CONTROLLERTAGS)

        await self.loadStandardDefinition()
        await loadModules(self.controller, self.opcua, self.modules, self.memory, self.mapping)

        devices = load_all_hardware(get_paths())
        for name, module in self.modules.items():
            for dev_id, info in devices.items():
                if module.CatalogNumber == dev_id:
                    if module.Vendor == info['data']['vendor']:
                        logging.debug(f"{dev_id}, {info}")

                        self.modulesLogic[name] = HWLogic(info['data'])

        await loadAoiDefinition(self.controller, self.opcua)
        await loadDataTypes(self.controller, self.opcua)

        await self.opcua.createDataTypes()

        self.results = {}

        await loadTags(self.controller, self.opcua, self.memory, self.mapping)
        await loadPrograms(self.controller, self._server, self.programs)

        self.safetyMap = SafetyMap(self.controller.find("./SafetyInfo/SafetyTagMap"))

        await self.opcua.createNodes(self.memory, self.mapping)

        await loadPrograms(self.controller, self._server, self.programs)

        loadTasks(self.controller, self.tasks)
        await PLCSYSTEM.init(self._server)

    async def loadStandardDefinition(self):
        items = list(DataTypeRegistry.getAll().items())

        for dataType, Definition in items:
            from datatypes.custom.datavariant import DataVariant
            struct = Structure(name=dataType, datavariant=issubclass(Definition, DataVariant))

            for name, field in get_ua_info(Definition).items():
                struct.fields.append(StructureField(name=name,
                                                    type=field.ua,
                                                    dimension=field.dim,
                                                    dataType=field.dataType))

            DataTypes.add(struct)

    async def UpdateOPCUA(self):
        for signal in self.mapping:
            await updateSignal(signal, self.memory)
       
        for signal in PLCSYSTEM.mapping:
            await updateSignal(signal, self.memory)

        for name, program in self.programs.items():
            for signal in program.mapping:
                await updateSignal(signal, program.memory)

    async def ReadOPCUA(self):
        for signal in self.mapping:
            updateMemory(signal, self.memory)

        for signal in PLCSYSTEM.mapping:
            updateMemory(signal, self.memory)

        for pname, program in self.programs.items():
            for signal in program.mapping:
                updateMemory(signal, program.memory)

    @subscribe_event(UpdateVariableEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def processQueue(self) -> None:
        try:
            while True:
                event = self.queue.get_nowait()
                if isinstance(event, UpdateVariableEvent):
                    if event.container == self.NAME:
                        self.memory.set(event.path, event.new_value)
                    elif event.container == PLCSYSTEM.NAME:
                        PLCSYSTEM.memory.set(event.path, event.new_value)
                    elif event.container in self.programs:
                        self.programs[event.container].memory.set(event.path, event.new_value)
        except Empty:
            pass

    async def mainloop(self):
        from core.memory.helper import setMemory, getMemory, OutputType
        await self.ReadOPCUA()

        self.processQueue()

        for standart, safety in self.safetyMap.Pairs.items():
            setMemory(safety, getMemory(standart, OutputType.PLC))

        for tname, task in self.tasks.items():
            await task.execute(programs=self.programs, context=self.context)

        if self.context.preScan:
            self.context.preScan = False
            setMemory("S:FS", True)
        elif self.context.postScan:
            self.context.postScan = False      
        else:
            setMemory("S:FS", False)

        for name, modulesLogic in self.modulesLogic.items():
            modulesLogic.update(name, self.memory)

        await self.UpdateOPCUA()

    def CallbackTypePostWrite(self, event:ServerItemCallback, dispatcher:CallbackService):
        if event.is_external:
            params = event.request_params
            if isinstance(params, WriteParameters):
                for node in params.NodesToWrite:
                    signal = self.mapping.getById(node.NodeId.Identifier)
                    if signal is not None:
                        signal.LAST_VALUE = node.Value.Value
                        self.mapping.add(signal)
                    else:
                        for pname, program in self.programs.items():
                            signal = program.mapping.getById(node.NodeId.Identifier)
                            if signal is not None:
                                signal.LAST_VALUE = node.Value.Value
                                program.mapping.add(signal)

    def stop(self):
        self._is_running = False