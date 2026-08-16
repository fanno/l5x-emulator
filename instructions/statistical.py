from typing import Any
import math
from dataclasses import dataclass, field
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.objectregistry import ObjectRegistry
from core.memory.identity import Identity
from datatypes.motion import MOVING_AVERAGE
from datatypes.capture import MINIMUM_CAPTURE, MAXIMUM_CAPTURE
from datatypes.custom.numbers import REAL
from datatypes.custom.array import Array
from engine.fbd.block import FBDBlock

from  instructions.helper import getPLCValue

@dataclass
class SAMPELMemory(Identity):
    SAMPELS:REAL = field(init=False, default_factory=REAL)

@InstructionRegistry.register
class MAVE(Instruction):

    def preScan(self, average:MOVING_AVERAGE, ctx:"ExecutionContext", storages:Array, weights:Array):
        average.EnableIn._reset()
        average.EnableOut._reset()

    def execute(self, average:MOVING_AVERAGE, ctx:"ExecutionContext", storages:Array, weights:Array) -> Any:
        if average.EnableIn:
            memory = ObjectRegistry.get(average, SAMPELMemory)


            number_of_samples = average.NumberOfSamples.getPLCValue()

            self.raiseNotImplementedError(ctx)
            
            if not average.EnableIn or number_of_samples < 1:
                samples = 0
            else:
                samples = memory.SAMPELS.getPLCValue()
            
                storages.insert(0, average.In.getPLCValue())
                storages.pop(number_of_samples)

                if samples < number_of_samples:
                    samples += 1

                total = 0.0

                limit = min(samples, number_of_samples)

                for i in range(limit):
                    if average.UseWeights:
                        total += storages[i] * weights[i]
                    else:
                        total += storages[i]

                if not average.UseWeights:
                    if samples > 0:
                        total = total / samples
                    else:
                        total = 0.0

                average.Out.setValue(total)

            average.EnableOut.setValue(average.EnableIn)

            memory.SAMPELS.setValue(samples)
        average.EnableOut.setValue(average.EnableIn)

    async def fbd_preScan(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        average:MOVING_AVERAGE = block.Value

        StorageArray = block.inParams["StorageArray"].Value
        WeightArray = block.inParams["WeightArray"].Value

        self.preScan(average, ctx, StorageArray, WeightArray)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        average:MOVING_AVERAGE = block.Value

        StorageArray = block.inParams["StorageArray"].Value
        WeightArray = block.inParams["WeightArray"].Value

        self.execute(average, ctx, StorageArray, WeightArray)

    async def st_preScan(self, ctx:"ExecutionContext") -> None:
        In:MOVING_AVERAGE = self.getMemory(self.args[0])
        StorageArray:Array = self.getMemory(self.args[1])
        WeightArray:Array = self.getMemory(self.args[2])

        self.preScan(In, ctx, StorageArray, WeightArray)

    async def st_execute(self, ctx:"ExecutionContext") -> None:
        In:MOVING_AVERAGE = self.getMemory(self.args[0])
        StorageArray:Array = self.getMemory(self.args[1])
        WeightArray:Array = self.getMemory(self.args[2])

        self.execute(In, ctx, StorageArray, WeightArray)

@InstructionRegistry.register
class MSTD(Instruction):

    def preScan(self, average:MOVING_AVERAGE, ctx:"ExecutionContext", storages:Array):
        average.EnableIn._reset()
        average.EnableOut._reset()

    def execute(self, average:MOVING_AVERAGE, ctx:"ExecutionContext", storages:Array) -> Any:
        if average.EnableIn:
            memory = ObjectRegistry.get(average, SAMPELMemory)

            number_of_samples = getPLCValue(average.NumberOfSamples)

            self.raiseNotImplementedError(ctx)

            if not average.EnableIn or number_of_samples < 1:
                samples = 0
            else:
                samples = getPLCValue(average.SAMPELS)

                storages.insert(0, getPLCValue(average.In))
                storages.pop(number_of_samples)

                if samples < number_of_samples:
                    samples += 1

                limit = min(samples, number_of_samples)

                sum_values = sum(storages[i] for i in range(limit))
                mean = sum_values / limit

                sum_sq_diff = 0.0
                for i in range(limit):
                    diff = storages[i] - mean
                    sum_sq_diff += diff * diff

                divisor = limit
                if limit > 1:
                    divisor = limit - 1

                variance = sum_sq_diff / divisor if divisor > 0 else 0.0

                std_dev = math.sqrt(variance) if variance >= 0 else 0.0

                average.Out.setValue(std_dev)

            average.EnableOut.setValue(average.EnableIn)

            memory.SAMPELS.setValue(samples)
        average.EnableOut.setValue(average.EnableIn)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        average:MOVING_AVERAGE = block.Value

        StorageArray = block.inParams["StorageArray"].Value

        self.execute(average, ctx, StorageArray)

    async def fbd_preScan(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        average:MOVING_AVERAGE = block.Value

        StorageArray = block.inParams["StorageArray"].Value

        self.preScan(average, ctx, StorageArray)

    async def fbd_execute(self, ctx:"ExecutionContext", block:FBDBlock) -> None:
        average:MOVING_AVERAGE = block.Value

        StorageArray = block.inParams["StorageArray"].Value

        self.execute(average, ctx, StorageArray)

    async def st_preScan(self, ctx:"ExecutionContext") -> None:
        In:MOVING_AVERAGE = self.getMemory(self.args[0])
        StorageArray:Array = self.getMemory(self.args[1])

        self.preScan(In, ctx, StorageArray)


    async def st_execute(self, ctx:"ExecutionContext") -> None:
        In:MOVING_AVERAGE = self.getMemory(self.args[0])
        StorageArray:Array = self.getMemory(self.args[1])

        self.execute(In, ctx, StorageArray)


@dataclass
class MMemory(Identity):
    Last:REAL = field(init=False, default_factory=REAL)

@InstructionRegistry.register
class MINC(Instruction):

    def preScan(self, min:MINIMUM_CAPTURE, ctx:"ExecutionContext"):
        min.EnableIn._reset()
        min.EnableOut._reset()

    def execute(self, min:MINIMUM_CAPTURE, ctx:"ExecutionContext") -> Any:    
        memory = ObjectRegistry.get(min, MMemory)

        if min.EnableIn:
            if min.Reset:
                min.Out.setValue(min.ResetValue)
                memory.Last.setValue(min.ResetValue)
            else:
                if min.EnableIn:
                    if min.In < memory.Last:
                        memory.Last.setValue(min.In)

        min.EnableOut.setValue(min.EnableIn)

@InstructionRegistry.register
class MAXC(Instruction):

    def preScan(self, max:MAXIMUM_CAPTURE, ctx:"ExecutionContext"):
        max.EnableIn._reset()
        max.EnableOut._reset()

    def execute(self, max:MAXIMUM_CAPTURE, ctx:"ExecutionContext") -> Any:    
        memory = ObjectRegistry.get(max, MMemory)

        if max.EnableIn:
            if max.Reset:
                max.Out.setValue(max.ResetValue)
                memory.Last.setValue(max.ResetValue)
            else:
                if max.EnableIn:
                    if max.In > memory.Last:
                        memory.Last.setValue(max.In)

        max.EnableOut.setValue(max.EnableIn)