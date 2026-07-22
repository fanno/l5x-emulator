import math
from dataclasses import dataclass, field
from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.objectregistry import ObjectRegistry
from core.memory.identity import Identity
from core.memory.helper import OutputType
from datatypes.motion import MOVING_AVERAGE, MOVING_STD_DEV
from datatypes.capture import MINIMUM_CAPTURE, MAXIMUM_CAPTURE
from datatypes.custom.numbers import REAL

from  instructions.helper import getPLCValue

@dataclass
class SAMPELMemory(Identity):
    SAMPELS:REAL = field(init=False, default_factory=REAL)

@InstructionRegistry.register
class MAVE(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        average:MOVING_AVERAGE = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(average, SAMPELMemory)

        number_of_samples = average.NumberOfSamples.getPLCValue()

        raise NotImplementedError(f"{__class__} not implemented yet")

        if not ctx.RungStatus or number_of_samples < 1:
            samples = 0
        else:
            samples = memory.SAMPELS.getPLCValue()

            storages:list[float] = self.getMemory(self.args[1])
            weights:list[float] = self.getMemory(self.args[2])
        
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

        memory.SAMPELS.setValue(samples)

@InstructionRegistry.register
class MSTD(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        average:MOVING_STD_DEV = self.getMemory(self.args[0])
        memory = ObjectRegistry.get(average, SAMPELMemory)

        number_of_samples = getPLCValue(average.NumberOfSamples)

        raise NotImplementedError(f"{__class__} not implemented yet")

        if not ctx.RungStatus or number_of_samples < 1:
            samples = 0
        else:
            samples = getPLCValue(average.SAMPELS)

            storages:list[float] = self.getMemory(self.args[1])

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

        memory.SAMPELS.setValue(samples)

@dataclass
class MMemory(Identity):
    Last:REAL = field(init=False, default_factory=REAL)

@InstructionRegistry.register
class MINC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        average:MINIMUM_CAPTURE = self.getMemory(self.args[0])

        memory = ObjectRegistry.get(average, MMemory)

        if average.Reset:
            average.Out.setValue(average.ResetValue)            
            memory.Last.setValue(average.ResetValue)
        else:
            if average.EnableIn:
                if average.In < memory.Last:
                    memory.Last.setValue(average.In)

        average.EnableOut.setValue(average.EnableIn)

@InstructionRegistry.register
class MAXC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        average:MAXIMUM_CAPTURE = self.getMemory(self.args[0])

        memory = ObjectRegistry.get(average, MMemory)

        if average.Reset:
            average.Out.setValue(average.ResetValue)            
            memory.Last.setValue(average.ResetValue)
        else:
            if average.EnableIn:
                if average.In > memory.Last:
                    memory.Last.setValue(average.In)

        average.EnableOut.setValue(average.EnableIn)