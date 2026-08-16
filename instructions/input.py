from typing import List

from core.registry.instructionregistry import InstructionRegistry
from core.controller import ProductCodes

from engine.context import ExecutionContext
from engine.instruction import Instruction
from engine.aoi.aoi import AOIRegistry
from engine.helper import CurrentProgramName, CurrentTaskName
from engine.context import EmulatorContext

from datatypes.custom.numbers import LINT, SINT, INT, DINT, UINT, UDINT, LINT, ULINT, USINT
from datatypes.custom.dt import DT
from datatypes.custom.array import isarray
from datatypes.custom.string import STRING
from datatypes.custom.bool import BOOL
from datatypes.custom.time import TIME32, TIME

from protocols.memory import SupportsGetPLCValue
from utils.isplcinstance import isPLCInstance

from instructions.helper import split_to_dint, splitArrayPath

@InstructionRegistry.register
class MSG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            source = self.args[0]
            ## TODO NEED TO be fixed
            self.raiseNotImplementedError(ctx)
        
@InstructionRegistry.register
class GSV(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Class = self.args[0]

            match Class:
                case 'AddOnInstructionDefinition':
                    instance = self.args[1]
                    attribute = self.args[2]
                    dest = self.getMemory(self.args[3])
                    aoi = AOIRegistry.get(instance)

                    source = getattr(aoi, attribute)

                    if type(dest) == type(source):
                        dest.setValue(source)
                        return
                case 'Axis':
                    instance = self.args[1]
                    attribute = self.args[2]
                    dest = self.getMemory(self.args[3])
                    from datatypes.axis import AXIS_CIP_DRIVE

                    aoi:AXIS_CIP_DRIVE = self.getMemory(self.args[1])
                    
                    v = getattr(aoi, attribute)

                    if isPLCInstance(v, SupportsGetPLCValue):
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
                    attribute = self.args[1]
                    match attribute:
                        case 'AuditValue':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)                            
                            if isinstance(dest, (LINT, ULINT)):
                                dest.setValue(0)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                        case 'ChangesToDetect':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            if isinstance(dest, (LINT, ULINT)):
                                dest.setValue(0)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                        case 'CanUseRPIFromProducer':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ControllerLogExecutionModificationCount':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ControllerLogTotalEntryCount':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'DataTablePadPercentage':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'IgnoreArrayFaultsDuringPostScan':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'InhibitAutomaticFirmwareUpdate':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, BOOL):
                                dest.setValue(True)
                                return
                        case 'KeepTestEditsOnSwitchOver':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'Name':
                            emulator = EmulatorContext.get()

                            dest = self.getMemory(self.args[2])

                            if isinstance(dest, STRING):
                                dest.setValue(emulator.DeviceName)
                                return
                        case 'RedundancyEnabled':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (SINT, USINT, INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'ShareUnusedTimeSlice':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'TimeSlice':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(10)
                                return
                case 'ControllerDevice':
                    attribute = self.args[1]

                    emulator = EmulatorContext.get()

                    match attribute:
                        case 'DeviceName':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            if isarray(dest, SINT, 33):
                                data:list[SINT] = []
                                if isarray(dest, SINT, emulator.DeviceName.LEN.getPLCValue()):
                                    index = 0
                                    while index < emulator.DeviceName.LEN:
                                        data.append(emulator.DeviceName[index])
                                        index += 1
                                    dest.setValue(data)
                                    return
                        case 'ProductCode':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(ProductCodes[emulator.DeviceName.getPLCValue()])
                                return
                        case 'ProductRev':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'SerialNumber':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'Status':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(int("0001000001100000", 2))
                                return
                        case 'Type':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(14)
                                return
                        case 'Vendor':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(1)
                                return
                case 'CoordinateSystem':
                    instance = self.args[1]
                    attribute = self.args[2]
                    dest = self.getMemory(self.args[3])
                case 'DataLog':
                    instance = self.args[1]
                    attribute = self.args[2]
                    dest = self.getMemory(self.args[3])
                case 'CST':
                    attribute = self.args[1]
                    match attribute:
                        case 'CurrentStatus':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'CurrentValue':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)

                            if isarray(dest, DINT, 2):
                                dest.setValue([DINT(0),DINT(0)])
                                return
                case 'DF1':
                    pass
                case 'FaultLog':
                    attribute = self.args[1]
                    match attribute:
                        case 'MajorEvents':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MajorFaultBits':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MinorEvents':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (INT, UINT, DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                        case 'MinorFaultBits':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, (DINT, UDINT, LINT, ULINT)):
                                dest.setValue(0)
                                return
                case 'HardwareStatus':
                    pass
                case 'Message':
                    instance = self.args[1]
                    attribute = self.args[2]
                    dest = self.getMemory(self.args[3])
                    pass
                case 'Module':
                    instance = self.args[1]
                    attribute = self.args[2]
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
                                key , _ = splitArrayPath(self.args[3])
                                dest = self.getMemory(key)

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

                                        while len(data) < len(dest):
                                            data.append(SINT(0))

                                        dest.setValue(data)
                                        return
                case 'MotionGroup':
                    instance = self.args[1]
                    attribute = self.args[2]
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
                    instance = self.args[1]
                    attribute = self.args[2]

                    emulator = EmulatorContext.get()

                    if instance == 'THIS':
                        instance = CurrentProgramName.get()

                    match attribute:
                        case 'DisableFlag':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, (SINT, DINT)):
                                dest.setValue(emulator.programs[instance].DisableFlag)
                                return                   
                        case 'LASTSCANTIME':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, (DINT, TIME32)):
                                dest.setValue(emulator.programs[instance].LASTSCANTIME)
                                return
                        case 'MAXSCANTIME':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, (DINT, TIME32)):
                                dest.setValue(emulator.programs[instance].MAXSCANTIME)
                                return
                        case 'MajorFaultRecord':
                            key , _ = splitArrayPath(self.args[3])
                            dest = self.getMemory(key)         
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'MinorFaultRecord':
                            key , _ = splitArrayPath(self.args[3])
                            dest = self.getMemory(key)                            
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'Name':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, STRING):
                                dest.setValue(emulator.programs[instance].Name)
                                return
                case 'Redundancy':
                    attribute = self.args[1]
                    dest = self.getMemory(self.args[2])
                case 'Routine':
                    instance = self.args[1]
                    attribute = self.args[2]
                    if instance == 'THIS':
                        RoutineRef = ctx.RoutineRef
                    else:
                        RoutineRef = ctx.ProgramRef.Routines[instance]

                    match attribute:
                        case 'INSTANCE':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(0)
                                return
                        case 'Name':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, STRING):
                                dest.setValue(RoutineRef.Name)
                                return
                        case 'SFCPaused':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, INT):
                                dest.setValue(RoutineRef.SFCResuming)
                                return
                        case 'SFCResuming':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, INT):
                                dest.setValue(RoutineRef.SFCResuming)
                                return
                case 'Safety':
                    attribute = self.args[1]
                    match attribute:
                        case 'SafetyLockedState':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySILConfiguration':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, SINT):
                                dest.setValue(2)
                                return
                        case 'SafetyStatus':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, INT):
                                dest.setValue(int("1000000000000000", 2))
                                return
                        case 'SafetySignatureExists':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySignatureID':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, SINT):
                                dest.setValue(0)
                                return
                        case 'SafetySignatureIDHex':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                        case 'SafetySignature':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                        case 'SafetyTaskFaultRecord':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            if isarray(dest, DINT, 11):
                                data:List[DINT] = []

                                while len(data) < 11:
                                    data.append(DINT(0))

                                dest.setValue(data)
                                return
                        case 'SafetySignatureIDLong':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            if isarray(dest, SINT, 33):
                                data:List[SINT] = []
                                
                                while len(data) < 33:
                                    data.append(SINT(0))

                                dest.setValue(data)
                                return
                        case 'SafetySignatureDateTime':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, STRING):
                                dest.setValue("")
                                return
                case 'SerialPort':
                    #TODO
                    pass
                case 'Task':
                    instance = self.args[1]
                    attribute = self.args[2]

                    emulator = EmulatorContext.get()

                    if instance == 'THIS':
                        instance = CurrentTaskName.get()

                    task = emulator.tasks[instance]

                    match attribute:
                        case 'DisableUpdateOutputs':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.DisableUpdateOutputs)
                                return
                        case 'EnableTimeOut':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.EnableTimeOut)
                                return
                        case 'InhibitTask':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.InhibitTask)
                                return
                        case 'LastScanTime':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.LastScanTime)
                                return
                        case 'INSTANCE':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(0)
                                return
                        case 'MaximumInterval':
                            dest = self.getMemory(self.args[3])
                            if isarray(dest, DINT, 2) or isarray(dest, TIME32, 2):
                                dest.setValue(split_to_dint(task.MaximumInterval))
                                return
                            if isinstance(dest, TIME):
                                dest.setValue(task.MaximumInterval)
                                return
                        case 'MaxScanTime':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.MaxScanTime)
                                return
                        case 'MinimumInterval':
                            key , _ = splitArrayPath(self.args[3])
                            dest = self.getMemory(key)

                            if isarray(dest, DINT, 2) or isarray(dest, TIME32, 2):
                                dest.setValue(split_to_dint(task.MinimumInterval))
                                return
                            if isinstance(dest, TIME):
                                dest.setValue(task.MinimumInterval)
                        case 'OverlapCount':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.OverlapCount)
                                return
                        case 'Priority':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, INT):
                                dest.setValue(task.Priority)
                                return
                        case 'Rate':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.Rate)
                                return
                        case 'StartTime':
                            key , _ = splitArrayPath(self.args[3])
                            dest = self.getMemory(key)

                            emulator = EmulatorContext.get()
                            
                            dt = emulator.clock.get_utc()

                            if isinstance(dest, (LINT, DT)):
                                dest.setValue(task.StartTime)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue(split_to_dint(task.StartTime))
                                return
                        case 'Status':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.Status)
                                return
                        case 'Watchdog':
                            dest = self.getMemory(self.args[3])
                            if isinstance(dest, DINT):
                                dest.setValue(task.Watchdog)
                                return
                case 'TimeSynchronize':
                    attribute = self.args[1]
                    dest = self.getMemory(self.args[2])
                case 'WallClockTime':
                    attribute = self.args[1]
                    match attribute:
                        case 'ApplyDST':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, SINT|INT|DINT):
                                emulator = EmulatorContext.get()
                            
                                dest.setValue(emulator.clock.get_dst())
                                return
                        case 'CSTOffset':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            emulator = EmulatorContext.get()
                            
                            offset = emulator.clock.offset()

                            if isinstance(dest, LINT):
                                dest.setValue(offset)
                                return
                            
                            if isarray(dest, DINT, 2):
                                dest.setValue(split_to_dint(offset))
                                return
                        case 'CurrentValue':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                    
                            emulator = EmulatorContext.get()
                            
                            dt = emulator.clock._get_utc()
                            if isinstance(dest, DT):
                                dest.setValue(dt)
                                return
                            timestamp = dt.timestamp() * 1000000
                            if isinstance(dest, LINT):
                                dest.setValue(timestamp)
                                return
                            if isarray(dest, DINT, 2):
                                dest.setValue(timestamp)
                                return
                        case 'DateTime':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)
                            if isarray(dest, DINT, 7):
                                emulator = EmulatorContext.get()
                            
                                dt = emulator.clock.get_utc()

                                for idx, item in enumerate(dest):
                                    item.setValue(dt[idx])

                                return
                        case 'LocalDateTime':
                            key , _ = splitArrayPath(self.args[2])
                            dest = self.getMemory(key)

                            if isarray(dest, DINT, 7):
                                emulator = EmulatorContext.get()
                            
                                dt = emulator.clock.get_local()

                                for idx, item in enumerate(dest):
                                    item.setValue(dt[idx])

                                return
                        case 'DSTAdjustment':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, INT):
                                #TODO
                                pass
                        case 'TimeZoneString':
                            dest = self.getMemory(self.args[2])
                            if isinstance(dest, INT):
                                #TODO
                                pass

            self.raiseNotImplementedError(ctx)
        
@InstructionRegistry.register
class SSV(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            Class = self.args[0]

            source = self.getMemory(self.args[3])
            match Class:
                case 'AddOnInstructionDefinition':
                    return
                case 'Axis':
                    instance = self.args[1]
                    attribute = self.args[2]
                    source = self.getMemory(self.args[3])
                case 'Controller':
                    attribute = self.args[1]
                    match attribute:
                        case 'ChangesToDetect':
                            key , _ = splitArrayPath(self.args[2])
                            source = self.getMemory(key)
                            if isinstance(source, LINT):
                                #TODO
                                pass
                            if isarray(source, DINT, 2):
                                #TODO
                                pass
                        case 'ControllerLogExecutionModificationCount':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, DINT):
                                #TODO
                                pass
                        case 'ControllerLogTotalEntryCount':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, DINT):
                                #TODO
                                pass
                        case 'IgnoreArrayFaultsDuringPostScan':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, SINT):
                                #TODO
                                pass
                        case 'InhibitAutomaticFirmwareUpdate':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, BOOL):
                                #TODO
                                pass
                        case 'KeepTestEditsOnSwitchOver':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, SINT):
                                #TODO
                                pass
                        case 'ShareUnusedTimeSlice':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                pass
                        case 'TimeSlice':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                pass
                case 'ControllerDevice':
                    pass
                case 'CoordinateSystem':
                    instance = self.args[1]
                    attribute = self.args[2]
                    source = self.getMemory(self.args[3])
                case 'CST':
                    pass
                case 'DF1':
                    #TODO
                    pass
                case 'FaultLog':
                    attribute = self.args[1]
                    match attribute:
                        case 'MajorEvents':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                return
                        case 'MajorFaultBits':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, DINT):
                                #TODO
                                return
                        case 'MinorEvents':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                return
                        case 'MinorFaultBits':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, DINT):
                                #TODO
                                return
                case 'HardwareStatus':
                    pass
                case 'Message':
                    instance = self.args[1]
                    attribute = self.args[2]
                    source = self.getMemory(self.args[3])
                case 'Module':
                    instance = self.args[1]
                    attribute = self.args[2]
                    
                    emulator = EmulatorContext.get()
                    match attribute:
                        case 'Mode':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, INT):
                                if source == 2:
                                    emulator.modules[instance].Inhibited.setValue(True)
                                else:
                                    emulator.modules[instance].Inhibited.setValue(False)
                                return
                case 'MotionGroup':
                    instance = self.args[1]
                    attribute = self.args[2]
                    source = self.getMemory(self.args[3])
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
                    instance = self.args[1]
                    attribute = self.args[2]
                    
                    emulator = EmulatorContext.get()

                    if instance == 'THIS':
                        instance = CurrentProgramName.get()

                    match attribute:
                        case 'DisableFlag':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, SINT):
                                emulator.programs[instance].DisableFlag.setValue(source)
                                return
                        case 'LASTSCANTIME':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, (DINT, TIME32)):
                                emulator.programs[instance].LASTSCANTIME.setValue(source)
                                return
                        case 'MAXSCANTIME':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, (DINT, TIME32)):
                                emulator.programs[instance].MAXSCANTIME.setValue(source)
                                return
                        case 'MajorFaultRecord':
                            key , _ = splitArrayPath(self.args[3])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 11):
                                #TODO
                                pass
                        case 'MinorFaultRecord':
                            key , _ = splitArrayPath(self.args[3])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 11):
                                #TODO
                                pass
                case 'Redundancy':
                    attribute = self.args[1]
                    source = self.getMemory(self.args[2])
                case 'Routine':
                    instance = self.args[1]
                    attribute = self.args[2]
                    source = self.getMemory(self.args[3])
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
                    instance = self.args[1]
                    attribute = self.args[2]
                    emulator = EmulatorContext.get()

                    if instance == 'THIS':
                        instance = CurrentTaskName.get()

                    task = emulator.tasks[instance]

                    match attribute:
                        case 'DisableUpdateOutputs':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.DisableUpdateOutputs.setValue(source)
                                return
                        case 'EnableTimeOut':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.EnableTimeOut.setValue(source)
                                return
                        case 'InhibitTask':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.InhibitTask.setValue(source)
                                return
                        case 'LastScanTime':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, (DINT, TIME32)):
                                task.LastScanTime.setValue(source)
                                return
                        case 'MaximumInterval':
                            key , _ = splitArrayPath(self.args[3])
                            source = self.getMemory(key)
                            
                            if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                #TODO
                                pass
                            if isinstance(source, TIME):
                                #TODO
                                pass
                        case 'MaxScanTime':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, (DINT, TIME32)):
                                task.MaxScanTime.setValue(source)
                                return
                        case 'MinimumInterval':
                            key , _ = splitArrayPath(self.args[3])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                #TODO
                                pass
                            if isinstance(source, TIME):
                                #TODO
                                pass
                        case 'OverlapCount':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.OverlapCount.setValue(source)
                        case 'Priority':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, INT):
                                task.Priority.setValue(source)
                                return
                        case 'Rate':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.Rate.setValue(source)
                                return
                        case 'StartTime':
                            key , _ = splitArrayPath(self.args[3])
                            source = self.getMemory(key)                            
                            if isarray(source, DINT, 2):
                                #TODO
                                pass
                            if isinstance(source, (DT, LINT)):
                                #TODO
                                pass
                        case 'Status':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, INT):
                                task.Status.setValue(source)
                                return
                        case 'Watchdog':
                            source = self.getMemory(self.args[3])
                            if isinstance(source, DINT):
                                task.Watchdog.setValue(source)
                                return
                case 'TimeSynchronize':
                    attribute = self.args[1]
                    dest = self.getMemory(self.args[2])
                case 'WallClockTime':
                    attribute = self.args[1]
                    match attribute:
                        case 'ApplyDST':
                            emulator = EmulatorContext.get()
                            source = self.getMemory(self.args[2])
                            if isinstance(source, SINT):
                                emulator.clock.set_dst(source != 0)
                                return
                        case 'CSTOffset':
                            key , _ = splitArrayPath(self.args[2])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 2) or isarray(source, TIME32, 2):
                                #TODO
                                pass
                            
                            if isinstance(source, TIME):
                                #TODO
                                pass
                        case 'CurrentValue':
                            key , _ = splitArrayPath(self.args[2])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 2):
                                #TODO
                                pass
                            
                            if isinstance(source, (DT, LINT)):
                                #TODO
                                pass
                        case 'DateTime':
                            key , _ = splitArrayPath(self.args[2])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 7):
                                #TODO
                                pass

                        case 'LocalDateTime':
                            key , _ = splitArrayPath(self.args[2])
                            source = self.getMemory(key)
                            if isarray(source, DINT, 7):
                                #TODO
                                pass
                        case 'DSTAdjustment':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                pass
                        case 'TimeZoneString':
                            source = self.getMemory(self.args[2])
                            if isinstance(source, INT):
                                #TODO
                                pass

            ## TODO NEED TO be fixed
            self.raiseNotImplementedError(ctx)
        
@InstructionRegistry.register
class IOT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        # ignore this as it is not relevant to simulation
        pass