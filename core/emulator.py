import logging
import asyncio
import threading
from queue import Queue, Empty
from typing import Dict, Union
from asyncua.common.callback import CallbackType, ServerItemCallback, CallbackService
from asyncua import Server
from asyncua.ua import WriteParameters
from lxml import etree
from lxml.etree import _ElementTree as ElementTree
from lxml.etree import _Element as Element

import instructions
import datatypes
import modules

from core.datatypes import get_ua_info, DataTypes
from core.registry.datatyperegistry import DataTypeRegistry
from core.memory.memory import Memory, PlcMemory
from core.memory.safetymap import SafetyMap
from core.events import LogEvent, StatusEvent, UpdateVariableEvent, StatusScan, StatusRequestEvent
from core.system import PLCSYSTEM
from core.constants import CONTROLLERTAGS
from core.signal import updateSignal, updateMemory
from core.xml.models import loadModules
from core.xml.tags import loadTags
from core.xml.datatypes import loadDataTypes
from core.xml.programs import loadPrograms
from core.xml.aoi import loadAoiDefinition
from core.xml.task import loadTasks
from core.library.libeary import initPyInstaller, load_all_hardware, get_paths
from core.library.hwlogic import HWLogic
from core.log import IndentedFormatter
from core.plcclock import PLCClock
from core.signal import Signal

T = Union[StatusEvent, UpdateVariableEvent]

from eventbus.eventbus import EventBus, EventListener, subscribe_event

from engine.context import EmulatorContext
from engine.program import Program
from engine.task import Task
from engine.errors import PLCFaultHandler
from engine.executiontimer import ExecutionTimer

from opcua.structure import Structure, StructureField
from opcua.tag import OpcuaTag
from opcua.mapping import Mapping

from datatypes.custom.module import MODULE
from datatypes.custom.string import STRING
from datatypes.custom.numbers import DINT

from protocols.memory import SupportsToUi
from utils.isplcinstance import isPLCInstance

class EmulatorLogHandler(logging.Handler):
    def __init__(self, level = 0):
        super().__init__(level)

    def emit(self, record):
        try:
            EventBus.get().dispatch(LogEvent(self.format(record), record.levelname))
        except Exception:
            pass

class Emulator(threading.Thread):
    PATH:str
    NAME:str

    programs:Dict[str, Program]
    tasks:Dict[str, Task]
    modules:Dict[str, MODULE]
    modulesLogic:Dict[str, HWLogic]

    memory:Memory
    mapping:Mapping
    tree:ElementTree
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

    preScan:bool = False
    postScan:bool = False
    scanCount:int = 0

    eventlistenet: EventListener

    forceOpcua:bool = False

    now:DINT

    OpcUaWriteTime:int
    OpcUaWriteTimeMax:int
    OpcUaReadTime:int
    OpcUaReadTimeMax:int

    statusRequestEvent:StatusRequestEvent

    clock:PLCClock

    in_plc_scan:bool

    _opcua_queue: Queue[tuple[Signal, Memory]]
    
    def __init__(self, path:str, port:int=4840, forceOpcua:bool=True):
        super().__init__()

        DataTypes.clear()
        from engine.aoi.aoi import AOIRegistry
        AOIRegistry.clear()
        from core.registry.instructionregistry import InstructionRegistry
        InstructionRegistry.clear_local()
        from core.registry.datatyperegistry import DataTypeRegistry
        DataTypeRegistry.clear_local()
        from core.registry.datauatypesregistry import DataUATypesRegistry
        DataUATypesRegistry.clear()
        from core.registry.datapythontypesregistry import DataPythonTypesRegistry
        DataPythonTypesRegistry.clear()

        self._is_running = False

        self.in_plc_scan = False

        initPyInstaller()

        self.queue = Queue()
        self._opcua_queue = Queue()

        self.programs = {}
        self.tasks = {}
        self.modules = {}
        self.modulesLogic = {}
        self.mapping = Mapping()
        self._server = Server()
        self.safetyMap = SafetyMap()
        self.clock = PLCClock()
        self.preScan = True
        self.postScan = False
        self.now = DINT()
        self.forceOpcua = forceOpcua

        self.OpcUaWriteTime = 0
        self.OpcUaWriteTimeMax = 0
        self.OpcUaReadTime = 0
        self.OpcUaReadTimeMax = 0 

        self.eventlistenet = EventListener(self)
        self.statusRequestEvent = StatusRequestEvent(Initial=True)

        self._loop = None
        self._throttle = 4

        gui_handler = EmulatorLogHandler(logging.WARNING)

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
        self.statusRequestEvent = StatusRequestEvent(Initial=True)

        EventBus.get().dispatch(StatusEvent(EndPoint=self._endpoint))

        self.tree = etree.parse(self.PATH, etree.XMLParser(strip_cdata=False))
        self.root = self.tree.getroot()

        self.controller = self.root.find("./Controller")

        self.setParameters()

        self.memory = Memory(NAME=self.NAME)
        PlcMemory.addContainer(self.memory)

    def setParameters(self):
        self.ProcessorType = STRING(self.controller.get("ProcessorType", ""))
        self.DeviceName = STRING(self.controller.get("Name", ""))

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._main())
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            logging.exception("An error occurred, in the server thread")
        finally:
            pass

    async def _main(self):
        EmulatorContext.set(self)
        self._is_running = True
        await self.init()
        await self._server.start()
        logging.info("Application started")
        logging.info(f"Server running at: {self._endpoint}")
        difTimeMax:float = 0.0
        lastDrawUi:float = 0.0
        scanDelayTime:float = 0.0

        average:float = 0.0

        while self._is_running:
            try:
                with PLCFaultHandler.major():
                    self.now.setValue(ExecutionTimer.get_ms())
                    timer = ExecutionTimer()
                    with timer:
                        await self.mainloop()
                        
                    scanDelayTime = 0.0

                    if not self.preScan and not self.postScan:
                        if (timer.elapsed > difTimeMax):
                            difTimeMax = timer.elapsed

                        if  self.scanCount > 0:
                            if average == 0:
                                average = timer.elapsed
                            average = average * (self.scanCount - 1) / self.scanCount + timer.elapsed / self.scanCount

                            scanDelayTime = average * self._throttle

                    if lastDrawUi < timer.start:
                        data = {}

                        if self.statusRequestEvent.Initial or True:
                            data[PLCSYSTEM.NAME] = {}
                            for key, variable in PLCSYSTEM.memory.getMemoryAll().items():
                                if isPLCInstance(variable, SupportsToUi):
                                    data[PLCSYSTEM.NAME][key] = variable.toUI(key)

                            data[self.NAME] = {}
                            for key, variable in self.memory.getMemoryAll().items():               
                                if isPLCInstance(variable, SupportsToUi):
                                    data[self.NAME][key] = variable.toUI(key)

                            for pname, program in self.programs.items():
                                data[program.Name] = {}
                                for key, variable in program.memory.getMemoryAll().items():
                                    if isPLCInstance(variable, SupportsToUi):
                                        data[program.Name][key] = variable.toUI(key)
                        else:
                            data[PLCSYSTEM.NAME] = {}
                            data[self.NAME] = {}
                            for pname, program in self.programs.items():
                                data[program.Name] = {}

                            if self.statusRequestEvent.Container:
                                container = None
                                if self.statusRequestEvent.Container == PLCSYSTEM.NAME:
                                    container = PLCSYSTEM.memory
                                elif self.statusRequestEvent.Container == self.NAME:
                                    container = self.memory
                                else:
                                    for pname, program in self.programs.items():
                                        if self.statusRequestEvent.Container == pname:
                                            container = program.memory
                                            break
                                    
                                if container is not None:
                                    for key, item in self.statusRequestEvent.Paths.items():
                                        value = container.get(key)
                                        if value is not None:
                                            if isPLCInstance(variable, SupportsToUi):
                                                data[self.statusRequestEvent.Container][key] = value.toUI(key, item)

                        taskStatus:dict[str, StatusScan] = {}
                        programStatus:dict[str, dict[str, StatusScan]] = {}
                        for tname, task in self.tasks.items():
                            taskStatus[tname] = StatusScan(Max=task.MaxScanTime.getPLCValue()/10000000, Last=task.LastScanTime.getPLCValue()/10000000, Count=task.scanCount)

                            programStatus[tname] = {}

                            for pname in task._programs:
                                program = self.programs[pname]
                                programStatus[tname][pname] = StatusScan(Max=program.MAXSCANTIME.getPLCValue()/10000000, Last=program.LASTSCANTIME.getPLCValue()/10000000)
                        
                        EventBus.get().dispatch(StatusEvent(Runing=True,
                                                StatusRequest=self.statusRequestEvent,
                                                Scan=StatusScan(Max=difTimeMax, Last=timer.elapsed, Count=self.scanCount),
                                                OpcUaRead=StatusScan(Max=self.OpcUaReadTimeMax/10000000, Last=self.OpcUaReadTime/10000000),
                                                OpcUaWrite=StatusScan(Max=self.OpcUaWriteTimeMax/10000000, Last=self.OpcUaWriteTime/10000000),
                                                Tasks=taskStatus,
                                                Programs=programStatus,
                                                ScanDelayed=scanDelayTime,
                                                ControllerName=self.DeviceName.getPLCValue(),
                                                ControllerType=self.ProcessorType.getPLCValue(),
                                                EndPoint=self._endpoint,
                                                Tags=data))

                        lastDrawUi = timer.start + 1

                    if timer.elapsed < scanDelayTime:
                        await asyncio.sleep(scanDelayTime-timer.elapsed)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                await self._server.stop()
                logging.exception(e)
                break
        self._is_running = False
        await self._server.stop()

    async def init(self):
        self._server.set_endpoint(self._endpoint)
        self._server.set_server_name("RockwellEmulator")
        await self._server.init()
        self._server.subscribe_server_callback(CallbackType.PostWrite, self.CallbackTypePostWrite)

        self.opcua = OpcuaTag(NAME=self.NAME,
                              SERVER=self._server,
                              memory=self.memory,
                              mapping=self.mapping)

        await self.opcua.registerNamespace("http://rockwell.plc")
        await self.opcua.createFolder(CONTROLLERTAGS)

        await self.loadStandardDefinition()
        await loadModules(self.controller, self.opcua, self.modules, self.memory, self.mapping)

        devices = load_all_hardware(get_paths())
        for name, module in self.modules.items():
            for dev_id, info in devices.items():
                if module.CatalogNumber == dev_id:
                    vendor = int(info['data']['vendor'], 16)
                    if module.Vendor == vendor:
                        logging.debug(f"Loaded HW module: {dev_id}, {info}")
                        self.modulesLogic[name] = HWLogic(info['data'])

        await loadAoiDefinition(self.controller, self.opcua)
        await loadDataTypes(self.controller, self.opcua)

        await self.opcua.createDataTypes()

        self.results = {}

        await loadTags(self.controller, self.opcua, self.memory, self.mapping)
        await loadPrograms(self.controller, self._server, self.programs)

        self.safetyMap = SafetyMap(self.controller.find("./SafetyInfo/SafetyTagMap"))

        await self.opcua.createNodes(self.forceOpcua)

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
        timer = ExecutionTimer()
        with timer:
            for update in self.opcua.updater:
                await updateSignal(update.signal, update.memory)
            self.opcua.updater.clear()

            for update in PLCSYSTEM.opcua.updater:
                await updateSignal(update.signal, update.memory)
            PLCSYSTEM.opcua.updater.clear()

            for name, program in self.programs.items():
                for update in program.opcua.updater:
                    await updateSignal(update.signal, update.memory)
                program.opcua.updater.clear()

        self.OpcUaWriteTime = timer.μs
        if self.OpcUaWriteTime > self.OpcUaWriteTimeMax:
            self.OpcUaWriteTimeMax = self.OpcUaWriteTime

    def ReadOPCUA(self):
        timer = ExecutionTimer()
        with timer:
            try:
                while True:
                    signal, memory = self._opcua_queue.get_nowait()
                    updateMemory(signal, memory, self.forceOpcua)
            except Empty:
                pass

        self.OpcUaReadTime = timer.μs
        if self.OpcUaReadTime > self.OpcUaReadTimeMax:
            self.OpcUaReadTimeMax = self.OpcUaReadTime

    @subscribe_event(UpdateVariableEvent, StatusRequestEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def processQueue(self) -> None:
        try:
            while True:
                event = self.queue.get_nowait()
                if isinstance(event, UpdateVariableEvent):
                    if event.Container == self.NAME:
                        self.memory.set(event.path, event.new_value)
                    elif event.Container == PLCSYSTEM.NAME:
                        PLCSYSTEM.memory.set(event.path, event.new_value)
                    elif event.Container in self.programs:
                        self.programs[event.Container].memory.set(event.path, event.new_value)
                elif isinstance(event, StatusRequestEvent):
                    self.statusRequestEvent = event
        except Empty:
            pass

    async def mainloop(self):
        from core.memory.helper import setMemory, getMemory, OutputType
        self.ReadOPCUA()

        self.in_plc_scan = True
        self.processQueue()
        for standart, safety in self.safetyMap.Pairs.items():
            setMemory(safety, getMemory(standart, OutputType.PLC))

        for tname, task in self.tasks.items():
            await task.execute(programs=self.programs)

        for name, modulesLogic in self.modulesLogic.items():
            modulesLogic.update(name, self.memory)

        self.in_plc_scan = False
        if self.preScan:
            self.preScan = False
            setMemory("S:FS", True)
        elif self.postScan:
            self.postScan = False
        else:
            self.scanCount += 1
            setMemory("S:FS", False)

        await self.UpdateOPCUA()

    def CallbackTypePostWrite(self, event:ServerItemCallback, dispatcher:CallbackService):
        if event.is_external:
            params = event.request_params
            if isinstance(params, WriteParameters):
                for node in params.NodesToWrite:
                    signal = self.mapping.getById(node.NodeId.Identifier)
                    if isinstance(signal, Signal):
                        signal.LAST_VALUE = node.Value.Value

                        self._opcua_queue.put((signal, self.memory))
                        #self.mapping.add(signal)
                    else:
                        for pname, program in self.programs.items():
                            signal = program.mapping.getById(node.NodeId.Identifier)
                            if isinstance(signal, Signal): 
                                signal.LAST_VALUE = node.Value.Value
                                self._opcua_queue.put((signal, program.memory))
                                #program.mapping.add(signal)

    def stop(self):
        self._is_running = False
        self.save()

    def shutdown(self):
        self.stop()

    def save(self):
        from utils.isplcinstance import isPLCInstance
        from protocols.memory import SupportsToL5X

        all = self.memory.getMemoryAll()
        for key, value in all.items():
            metadata = self.memory.get_metadata(key)
            if metadata:
                element = metadata.XMlElement
                if isinstance(element , Element):
                    value = self.memory.get(key)
                    if isPLCInstance(value, SupportsToL5X):
                        value.toL5X(element)

        self.tree.write(
            "saved.L5X",
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
            standalone=True
        )
