from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from engine.aoi.aoi import AOIRegistry

from datatypes.custom.numbers import LINT, SINT, INT, DINT, UINT, UDINT, LINT, ULINT, USINT
from datatypes.custom.dt import DT
from datatypes.custom.array import Array, isarray
from datatypes.custom.string import STRING
from datatypes.custom.bool import BOOL
from datatypes.custom.time import TIME32, TIME
from datatypes.custom.datavariant import DataVariant

from core.system import PLCSYSTEM
from core.controller import ProductCodes

from typing import List

from instructions.helper import split_to_dint

from engine.helper import CurrentProgramName, CurrentTaskName

@InstructionRegistry.register
class MSG(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            source = self.args[0]
            ## TODO NEED TO be fixed
            raise NotImplementedError(f"{__class__} not implemented yet")
        
@InstructionRegistry.register
class GSV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Class = self.args[0]
            instance = self.args[1]
            attribute = self.args[2]

            match Class:
                case 'AddOnInstructionDefinition':
                    dest = self.getMemory(self.args[3])
                    aoi = AOIRegistry.get(instance)

                    source = getattr(aoi, attribute)

                    if type(dest) == type(source):
                        dest.setValue(source)
                        return
                case 'Axis':
                    dest = self.getMemory(self.args[3])
                    from datatypes.axis import AXIS_CIP_DRIVE

                    aoi:AXIS_CIP_DRIVE = self.getMemory(self.args[1])
                    
                    v = getattr(aoi, attribute)

                    if isinstance(v, DataVariant):
                        dest.setValue(v.getPLCValue())
                        return

                    '''
                    match attribute:
                        case 'SoftTravelLimitNegative':
                            dest.setValue(aoi.SoftTravelLimitNegative.getPLCValue())
                            return
                        case 'SoftTravelLimitPositive':
                            dest.setValue(aoi.SoftTravelLimitPositive.getPLCValue())
                            return
                    '''
                            
                case 'Controller':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'AuditValue':
                            if isinstance(dest, (LINT, ULINT)):
                                dest.setValue(0)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                        case 'ChangesToDetect':
                            if isinstance(dest, (LINT, ULINT)):
                                dest.setValue(0)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                        case 'CanUseRPIFromProducer':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ControllerLogExecutionModificationCount':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ControllerLogTotalEntryCount':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'DataTablePadPercentage':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'IgnoreArrayFaultsDuringPostScan':
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'InhibitAutomaticFirmwareUpdate':
                            if isinstance(dest, BOOL):
                                dest.setValue(True)
                                return
                        case 'KeepTestEditsOnSwitchOver':
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'Name':
                            from core.emulator import Emulator
                            from core.servicelocator import ServiceLocator
                            emulator = ServiceLocator.get(Emulator)

                            if isinstance(dest, STRING):
                                dest.setValue(emulator.DeviceName)
                                return
                        case 'RedundancyEnabled':
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ShareUnusedTimeSlice':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'TimeSlice':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(10)
                                return
                case 'ControllerDevice':
                    dest = self.getMemory(self.args[3])

                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)

                    match attribute:
                        case 'DeviceName':
                            if isarray(dest, SINT, 33):
                                emulator.DeviceName
                                data:list[SINT] = []
                                if isarray(dest, SINT, emulator.DeviceName.LEN.getPLCValue()):
                                    index = 0
                                    while index < emulator.DeviceName.LEN:
                                        data.append(emulator.DeviceName[index])
                                        index += 1
                                    dest.setValue(data)
                                    return
                        case 'ProductCode':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(ProductCodes[emulator.DeviceName.getPLCValue()])
                                return
                        case 'ProductRev':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'SerialNumber':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'Status':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(int("0001000001100000", 2))
                                return
                        case 'Type':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(14)
                                return
                        case 'Vendor':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(1)
                                return
                case 'CoordinateSystem':
                    pass
                case 'CST':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'CurrentStatus':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'CurrentValue':
                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                case 'DF1':
                    pass
                case 'FaultLog':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'MajorEvents':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MajorFaultBits':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MinorEvents':
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MinorFaultBits':
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                case 'HardwareStatus':
                    pass
                case 'Message':
                    pass
                case 'Module':
                    from datatypes.custom.module import MODULE
                    module = self.getMemory(instance)
                    if isinstance(module, MODULE):
                        match attribute:
                            case 'EntryStatus':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    if not module.Inhibited:
                                        dest.setValue(int("4000", 16))
                                    else:
                                        dest.setValue(int("6000", 16))
                                    return
                            case 'FaultCode':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(0)
                                    return
                            case 'FaultInfo':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(0)
                                    return
                            case 'FirmwareSupervisorStatus':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(0)
                                    return
                            case 'ForceStatus':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(0)
                                    return
                            case 'INSTANCE':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(0)
                                    return
                            case 'LedStatus':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    dest.setValue(3)
                                    return
                            case 'Mode':
                                dest = self.getMemory(self.args[3])
                                if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                    if not module.Inhibited:
                                        dest.setValue(0)
                                    else:
                                        dest.setValue(2)
                                    return
                            case 'Path':
                                destination, _ = self.args[3].split("[", 1)

                                dest = self.getMemory(destination)

                                if isarray(dest, SINT, 2):
                                    address = None
                                    for port in module.Ports:
                                        if port.Type == "Ethernet":
                                            address = port.Address
                                            break

                                    if address:
                                        data:list[SINT] = []
                                        if isarray(dest, SINT, address.LEN.getPLCValue() + 2):
                                            data.append(SINT(address.LEN))
                                            data.append(SINT(0))
                                            index = 0
                                            while index < address.LEN:
                                                data.append(address[index])
                                                index += 1
                                        else:
                                            data.append(SINT(0))
                                            data.append(SINT(0))
                                        dest.setValue(data)
                                        return
                case 'MotionGroup':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'Alternate1UpdateMultiplier':
                            # SINT INT DINT
                            pass
                        case 'Alternate1UpdatePeriod':
                            # DINT
                            pass
                        case 'Alternate2UpdateMultiplier':
                            # SINT INT DINT
                            pass
                        case 'Alternate2UpdatePeriod':
                            # DINT
                            pass
                        case 'AutoTagUpdate':
                            # SINT INT DINT
                            pass
                        case 'CoarseUpdatePeriod':
                            # DINT
                            pass
                        case 'CycleStartTime':
                            # DT LINT DINT[2]
                            pass
                        case 'INSTANCE':
                            # DINT
                            pass
                        case 'MaximumInterval':
                            # TIME TIME32[2] DINT[2]
                            pass
                        case 'MinimumInterval':
                            # TIME TIME32[2] DINT[2]
                            pass
                        case 'StartTime':
                            # DT LINT DINT[2]
                            pass
                        case 'TaskAverageIOTime':
                            # TIME32 DINT
                            pass
                        case 'TaskAverageScanTime':
                            # TIME32 DINT
                            pass
                        case 'TaskLastIOTime':
                            # TIME32 DINT
                            pass
                        case 'TaskLastScanTime':
                            # TIME32 DINT
                            pass
                        case 'TaskMaximumIOTime':
                            # TIME32 DINT
                            pass
                        case 'TaskMaximumScanTime':
                            # TIME32 DINT
                            pass
                        case 'TimeOffset':
                            # TIME32 DINT
                            pass
                case 'Program':
                    dest = self.getMemory(self.args[3])

                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)

                    if instance == 'THIS':
                        instance = CurrentProgramName.get()

                    match attribute:
                        case 'DisableFlag':
                            if isinstance(dest, (SINT, DINT)):
                                dest.setValue(emulator.programs[instance].DisableFlag)
                                return                   
                        case 'LASTSCANTIME':
                            if isinstance(dest, (DINT, TIME32)):
                                dest.setValue(emulator.programs[instance].LASTSCANTIME)
                                return
                        case 'MAXSCANTIME':
                            if isinstance(dest, (DINT, TIME32)):
                                dest.setValue(emulator.programs[instance].MAXSCANTIME)
                                return
                        case 'MajorFaultRecord':
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'MinorFaultRecord':
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'Name':
                            if isinstance(dest, STRING):
                                dest.setValue(emulator.programs[instance].Name)
                                return
                case 'Redundancy':
                    pass
                case 'Routine':
                    dest = self.getMemory(self.args[3])
                    if instance == 'THIS':
                        RoutineRef = ctx.RoutineRef
                    else:
                        RoutineRef = ctx.ProgramRef.Routines[instance]

                    match attribute:
                        case 'INSTANCE':
                            if isinstance(dest, DINT):
                                dest.setValue(0)
                                return
                        case 'Name':
                            if isinstance(dest, STRING):
                                dest.setValue(RoutineRef.Name)
                                return
                        case 'SFCPaused':
                            if isinstance(dest, INT):
                                dest.setValue(RoutineRef.SFCResuming)
                                return
                        case 'SFCResuming':
                            if isinstance(dest, INT):
                                dest.setValue(RoutineRef.SFCResuming)
                                return
                case 'Safety':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'SafetyLockedState':
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySILConfiguration':
                            if isinstance(dest, SINT):
                                dest.setValue(2)
                                return
                        case 'SafetyStatus':
                            if isinstance(dest, INT):
                                dest.setValue(int("1000000000000000", 2))
                                return
                        case 'SafetySignatureExists':
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySignatureID':
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySignatureIDHex':
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                        case 'SafetySignature':
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                        case 'SafetyTaskFaultRecord':
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'SafetySignatureIDLong':
                            if isarray(dest, SINT, 33):
                                data:List[SINT] = []
                                
                                while len(data) < 33:
                                    data.append(SINT(0))

                                dest.setValue(data)
                                return
                        case 'SafetySignatureDateTime':
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                case 'SerialPort':
                    #TODO
                    pass
                case 'Task':
                    dest = self.getMemory(self.args[3])

                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)

                    if instance == 'THIS':
                        instance = CurrentTaskName.get()

                    task = emulator.tasks[instance]

                    match attribute:
                        case 'DisableUpdateOutputs':
                            if isinstance(dest, DINT):
                                dest.setValue(task.DisableUpdateOutputs)
                                return
                        case 'EnableTimeOut':
                            if isinstance(dest, DINT):
                                dest.setValue(task.EnableTimeOut)
                                return
                        case 'InhibitTask':
                            if isinstance(dest, DINT):
                                dest.setValue(task.InhibitTask)
                                return
                        case 'LastScanTime':
                            if isinstance(dest, DINT):
                                dest.setValue(task.LastScanTime)
                                return
                        case 'INSTANCE':
                            if isinstance(dest, DINT):
                                dest.setValue(0)
                                return
                        case 'MaximumInterval':
                            if isarray(dest, DINT, 2) or isarray(dest, TIME32, 2):
                                dest.setValue(split_to_dint(task.MaximumInterval))
                                return
                            if isinstance(dest, TIME):
                                dest.setValue(task.MaximumInterval)
                                return
                        case 'MaxScanTime':
                            if isinstance(dest, DINT):
                                dest.setValue(task.MaxScanTime)
                                return
                        case 'MinimumInterval':
                            if isarray(dest, DINT, 2) or isarray(dest, TIME32, 2):
                                dest.setValue(split_to_dint(task.MinimumInterval))
                                return
                            if isinstance(dest, TIME):
                                dest.setValue(task.MinimumInterval)
                        case 'OverlapCount':
                            if isinstance(dest, DINT):
                                dest.setValue(task.OverlapCount)
                                return
                        case 'Priority':
                            if isinstance(dest, INT):
                                dest.setValue(task.Priority)
                                return
                        case 'Rate':
                            if isinstance(dest, DINT):
                                dest.setValue(task.Rate)
                                return
                        case 'StartTime':
                            dt = PLCSYSTEM.clock.utcnow()

                            if isinstance(dest, (LINT, DT)):
                                dest.setValue(task.StartTime)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue(split_to_dint(task.StartTime))
                                return
                        case 'Status':
                            if isinstance(dest, DINT):
                                dest.setValue(task.Status)
                                return
                        case 'Watchdog':
                            if isinstance(dest, DINT):
                                dest.setValue(task.Watchdog)
                                return
                case 'TimeSynchronize':
                    pass
                case 'WallClockTime':
                    dest = self.getMemory(self.args[3])
                    match attribute:
                        case 'ApplyDST':
                            if isinstance(dest, SINT):
                                dest.setValue(PLCSYSTEM.clock.dst)
                                return
                        case 'CSTOffset':
                            offset = PLCSYSTEM.clock.offset
                            if isinstance(dest, LINT):
                                dest.setValue(offset)
                                return
                            
                            if isarray(dest, DINT, 2):
                                dest.setValue(split_to_dint(offset))
                                return
                        case 'CurrentValue':
                            dt = PLCSYSTEM.clock.utcnow()

                            if isinstance(dest, DT):
                                dest.setValue(dt)
                                return
                            timestamp = dt.timestamp()
                            if isinstance(dest, LINT):
                                dest.setValue(dt.timestamp(timestamp))
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue(split_to_dint(timestamp))
                                return
                        case 'DateTime':
                            if isarray(dest, DINT, 7):
                                dt = PLCSYSTEM.clock.utcnow()

                                data:List[DINT] = []
                                data[0] = DINT(dt.year)
                                data[1] = DINT(dt.month)
                                data[2] = DINT(dt.day)
                                data[3] = DINT(dt.hour)
                                data[4] = DINT(dt.min)
                                data[5] = DINT(dt.second)
                                data[6] = DINT(dt.microsecond)

                                dest.setValue(data)
                                return
                        case 'LocalDateTime':
                            if isarray(dest, DINT, 7):
                                dt = PLCSYSTEM.clock.now()

                                data:List[DINT] = []
                                data[0] = DINT(dt.year)
                                data[1] = DINT(dt.month)
                                data[2] = DINT(dt.day)
                                data[3] = DINT(dt.hour)
                                data[4] = DINT(dt.min)
                                data[5] = DINT(dt.second)
                                data[6] = DINT(dt.microsecond)

                                dest.setValue(data)
                                return
                        case 'DSTAdjustment':
                            if isinstance(dest, INT):
                                #TODO
                                pass
                        case 'TimeZoneString':
                            if isinstance(dest, INT):
                                #TODO
                                pass

            raise NotImplementedError(f"{__class__} not implemented yet: {self.args}")
        
@InstructionRegistry.register
class SSV(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            Class = self.args[0]
            instance = self.args[1]
            attribute = self.args[2]

            source = self.getMemory(self.args[3])
            match Class:
                case 'AddOnInstructionDefinition':
                    if isinstance(source, DataVariant):
                        aoi = AOIRegistry.get(instance)

                        dest = getattr(aoi, attribute)

                        if isinstance(dest, DataVariant):
                            if type(source) == type(dest):
                                dest.setValue(source)
                                return
                case 'Axis':
                    pass
                case 'Controller':
                    match attribute:
                        case 'ChangesToDetect':
                            if isinstance(source, LINT):
                                #TODO
                                pass
                            if isarray(source, DINT, 2):
                                #TODO
                                pass
                        case 'ControllerLogExecutionModificationCount':
                            if isinstance(source, DINT):
                                #TODO
                                pass
                        case 'ControllerLogTotalEntryCount':
                            if isinstance(source, DINT):
                                #TODO
                                pass
                        case 'IgnoreArrayFaultsDuringPostScan':
                            if isinstance(source, SINT):
                                #TODO
                                pass
                        case 'InhibitAutomaticFirmwareUpdate':
                            if isinstance(source, BOOL):
                                #TODO
                                pass
                        case 'KeepTestEditsOnSwitchOver':
                            if isinstance(source, SINT):
                                #TODO
                                pass
                        case 'ShareUnusedTimeSlice':
                            if isinstance(source, INT):
                                #TODO
                                pass
                        case 'TimeSlice':
                            if isinstance(source, INT):
                                #TODO
                                pass
                case 'ControllerDevice':
                    pass
                case 'CoordinateSystem':
                    pass
                case 'CST':
                    pass
                case 'DF1':
                    #TODO
                    pass
                case 'FaultLog':
                    match attribute:
                        case 'MajorEvents':
                            if isinstance(source, INT):
                                #TODO
                                return
                        case 'MajorFaultBits':
                            if isinstance(source, DINT):
                                #TODO
                                return
                        case 'MinorEvents':
                            if isinstance(source, INT):
                                #TODO
                                return
                        case 'MinorFaultBits':
                            if isinstance(source, DINT):
                                #TODO
                                return
                case 'HardwareStatus':
                    pass
                case 'Message':
                    pass
                case 'Module':
                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)
                    match attribute:
                        case 'Mode':
                            if isinstance(source, INT):
                                if source == 2:
                                    emulator.modules[instance].Inhibited.setValue(True)
                                else:
                                    emulator.modules[instance].Inhibited.setValue(False)
                                return
                case 'MotionGroup':
                    match attribute:
                        case 'AutoTagUpdate':
                            # SINT INT DINT
                            #TODO
                            pass
                        case 'MaximumInterval':
                            # TIME TIME32[2] DINT[2]
                            #TODO
                            pass
                        case 'TaskAverageIOTime':
                            # TIME32 DINT
                            #TODO
                            pass
                        case 'TaskAverageScanTime':
                            # TIME32 DINT
                            #TODO
                            pass
                        case 'TaskMaximumIOTime':
                            # TIME32 DINT
                            #TODO
                            pass
                        case 'TaskMaximumScanTime':
                            # TIME32 DINT
                            #TODO
                            pass
                case 'Program':
                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)

                    if instance == 'THIS':
                        instance = CurrentProgramName.get()

                    match attribute:
                        case 'DisableFlag':
                            if isinstance(source, SINT):
                                emulator.programs[instance].DisableFlag.setValue(source)
                                return
                        case 'LASTSCANTIME':
                            if isinstance(source, (DINT, TIME32)):
                                emulator.programs[instance].LASTSCANTIME.setValue(source)
                                return
                        case 'MAXSCANTIME':
                            if isinstance(source, (DINT, TIME32)):
                                emulator.programs[instance].MAXSCANTIME.setValue(source)
                                return
                        case 'MajorFaultRecord':
                            if isarray(source, DINT, 11):
                                #TODO
                                pass
                        case 'MinorFaultRecord':
                            if isarray(source, DINT, 11):
                                #TODO
                                pass
                case 'Redundancy':
                    pass
                case 'Routine':
                    if instance == 'THIS':
                        RoutineRef = ctx.RoutineRef
                    else:
                        RoutineRef = ctx.ProgramRef.Routines[instance]

                    match attribute:
                        case 'SFCResuming':
                            if isinstance(source, INT):
                                RoutineRef.SFCResuming.setValue(source)
                                return
                case 'Safety':
                    pass
                case 'SerialPort':
                    #TODO
                    pass
                case 'Task':
                    from core.emulator import Emulator
                    from core.servicelocator import ServiceLocator
                    emulator = ServiceLocator.get(Emulator)

                    if isinstance(emulator, Emulator):
                        if instance == 'THIS':
                            instance = CurrentTaskName.get()

                        task = emulator.tasks[instance]

                        match attribute:
                            case 'DisableUpdateOutputs':
                                if isinstance(source, DINT):
                                    task.DisableUpdateOutputs.setValue(source)
                                    return
                            case 'EnableTimeOut':
                                if isinstance(source, DINT):
                                    task.EnableTimeOut.setValue(source)
                                    return
                            case 'InhibitTask':
                                if isinstance(source, DINT):
                                    task.InhibitTask.setValue(source)
                                    return
                            case 'LastScanTime':
                                if isinstance(source, (DINT, TIME32)):
                                    task.LastScanTime.setValue(source)
                                    return
                            case 'MaximumInterval':
                                if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                    #TODO
                                    pass
                                if isinstance(source, TIME):
                                    #TODO
                                    pass
                            case 'MaxScanTime':
                                if isinstance(source, (DINT, TIME32)):
                                    task.MaxScanTime.setValue(source)
                                    return
                            case 'MinimumInterval':
                                if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                    #TODO
                                    pass
                                if isinstance(source, TIME):
                                    #TODO
                                    pass
                            case 'OverlapCount':
                                if isinstance(source, DINT):
                                    task.OverlapCount.setValue(source)
                            case 'Priority':
                                if isinstance(source, INT):
                                    task.Priority.setValue(source)
                                    return
                            case 'Rate':
                                if isinstance(source, DINT):
                                    task.Rate.setValue(source)
                                    return
                            case 'StartTime':
                                if isarray(source, DINT, 2):
                                    #TODO
                                    pass
                                if isinstance(source, (DT, LINT)):
                                    #TODO
                                    pass
                            case 'Status':
                                if isinstance(source, INT):
                                    task.Status.setValue(source)
                                    return
                            case 'Watchdog':
                                if isinstance(source, DINT):
                                    task.Watchdog.setValue(source)
                                    return
                case 'TimeSynchronize':
                    pass
                case 'WallClockTime':
                    match attribute:
                        case 'ApplyDST':
                            if isinstance(source, SINT):
                                if source == 0:
                                    PLCSYSTEM.clock.dst = False
                                else:
                                    PLCSYSTEM.clock.dst = True
                                return
                        case 'CSTOffset':
                            if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                #TODO
                                pass
                            
                            if isinstance(source, TIME):
                                #TODO
                                pass
                        case 'CurrentValue':
                            if isarray(source, DINT, 2):
                                #TODO
                                pass
                            
                            if isinstance(source, (DT, LINT)):
                                #TODO
                                pass
                        case 'DateTime':
                            if isarray(source, DINT, 7):
                                #TODO
                                pass

                        case 'LocalDateTime':
                            if isarray(source, DINT, 7):
                                #TODO
                                pass
                        case 'DSTAdjustment':
                            if isinstance(source, INT):
                                #TODO
                                pass
                        case 'TimeZoneString':
                            if isinstance(source, INT):
                                #TODO
                                pass

            ## TODO NEED TO be fixed
            raise NotImplementedError(f"{__class__} not implemented yet")
        
@InstructionRegistry.register
class IOT(Instruction):

    async def execute(self, ctx:"ExecutionContext") -> None:
        # ignore this as it is not relevant to simulation
        pass