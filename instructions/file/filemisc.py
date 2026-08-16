from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry

from datatypes.misc import CONTROL
from datatypes.custom.array import Array
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.string import STRING

from  instructions.helper import getPLCValue, splitArrayPath

from protocols.memory import SupportsSetValue
from utils.isplcinstance import isPLCInstance

@InstructionRegistry.register
class FAL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)
        
            '''
            control:CONTROL = self.getMemory(self.args[0])
            mode = self.args[1]
            
            dst = self.getMemory(self.args[2])
            operation = self.getMemory(self.args[3])
            length = getPLCValue(self.getMemory(self.args[4]))

            for i in range(min(length, len(src))):
            
                dst[i] = operation(src[i])

            self.setMemory(self.args[1], dst)
            '''

@InstructionRegistry.register
class FSC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:

            self.raiseNotImplementedError(ctx)
            '''
            control:CONTROL = self.getMemory(self.args[0])
            array = self.getMemory(self.args[1])
            target = self.getMemory(self.args[2])
            dest = self.args[3]

            index = -1
            for i, val in enumerate(array):
                if val == target:
                    index = i
                    break

            self.setMemory(dest, index)
            '''

@InstructionRegistry.register
class COP(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            length = getPLCValue(self.getMemory(self.args[2]))

            if length > 0:
                src_path , src_dims = splitArrayPath(self.args[0])
                dest_path , dest_dims = splitArrayPath(self.args[1])


                dest = self.getMemory(dest_path)

                if len(src_dims)  > 1 or len(dest_dims) > 1:
                    raise NotImplementedError(f"{__class__} Multi-dimensional arrays not yet implemented")

                if length == 1:
                    source = self.getMemory(self.args[0])
                    dest = self.getMemory(self.args[1])
                    if type(source) == type(dest):
                        dest.setValue(source)
                        return
                else:
                    source = self.getMemory(src_path)
                    for item in src_dims[:-1]:
                        source = source[item]
                    if not isinstance(source, Array):
                        return
                
                    src_start = src_dims[-1]
                    src_end = src_start + (length -1)

                    if len(source) <= src_end:
                        raise IndexError(f"{__class__} Source array overflow: {length} {src_start} -> {src_end}")

                    dest = self.getMemory(dest_path)
                    for item in dest_dims[:-1]:
                        dest = dest[item]

                    if not isinstance(dest, Array):
                        return

                    dest_start = dest_dims[-1]
                    dest_end = dest_start + (length -1)
                    if len(dest) <= dest_end:
                        raise IndexError(f"{__class__} Source array overflow: {length} {dest_start} -> {dest_end}")                    

                    for idx in range(length):
                        if isinstance(source, Array):
                            s = source[src_start+idx]
                            d = dest[dest_start+idx]
                            if type(s) == type(d):
                                if isPLCInstance(d, SupportsSetValue):
                                    d.setValue(s)
                    return

                raise NotImplementedError(f"{__class__} Case not implemented {self.args}")

@InstructionRegistry.register
class CPS(COP):
    #TODO: cop and CPS is "identical", not sure how to implement memory lock while doing the copy
    pass                        

@InstructionRegistry.register
class FLL(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            dest_path , dest_dims = splitArrayPath(self.args[1])
            length = getPLCValue(self.getMemory(self.args[2]))

            if length > 0:
                source = self.getMemory(self.args[0])
                dest = self.getMemory(dest_path)

                if len(dest_dims) > 1:
                    raise NotImplementedError(f"{__class__} Multi-dimensional arrays not yet implemented")
            
                if not dest_dims:
                    dest.setValue(source)
                else:
                    if dest_dims:
                        dest_start = dest_dims[0]

                        if dest_start + length > len(dest):
                            raise IndexError(f"{__class__} Destination array overflow: {dest_start} + {length}")

                        for i in range(length):
                            d = dest[dest_start + i]
                            if type(source) != type(d):
                                raise TypeError(f"{__class__} Source and dest not the same, {type(source)}, {type(d)}")

                            d.setValue(source)
                    else:
                        if length != 1:
                            raise ValueError(f"{__class__} Array→scalar requires length=1, got {length}")

                        if type(source) != type(dest):
                            raise TypeError(f"{__class__} Source and dest not the same")
                        
                        dest.setValue(source)

@InstructionRegistry.register
class AVE(Instruction):

    async def ladder_preScan(self, ctx):
        control:CONTROL = self.getMemory(self.args[3])

        control.EnableIn._reset()
        control.EnableOut._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        control:CONTROL = self.getMemory(self.args[3])

        if ctx.RLL.RungStatus:
            arrayName , dims = splitArrayPath(self.args[0])
            array = self.getMemory(arrayName)

            if len(dims) > 1:
                raise NotImplementedError(f"{__class__} 2d/3d array, not implemented yet")
            
            arrayDim = array.getDim()

            dim = self.getMemory(self.args[1])
            dest:DataVariant = self.getMemory(self.args[2])

            added = 0.0
            size = 1
            if dim == 0:
                size = 0
                for index in range(dims[0], arrayDim[0]):
                    added += array[index].getPLCValue()
                    size += 1
            elif dim == 1:
                raise NotImplementedError(f"{__class__} dim 1, not implemented yet")
            elif dim == 2:
                raise NotImplementedError(f"{__class__} dim 2, not implemented yet")
                
            dest.setValue(added/size)
        else:
            if control.DN:
                if not control.ER:
                    control.EN.setValue(False)
                    control.ER.setValue(False)
                    control.DN.setValue(False)
                    control.POS.setValue(0)

@InstructionRegistry.register
class SRT(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class STD(Instruction):

    async def ladder_preScan(self, ctx):
        control:CONTROL = self.getMemory(self.args[3])

        control.EN._reset()
        control.DN._reset()
        control.ER._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            control:CONTROL = self.getMemory(self.args[3])

            self.raiseNotImplementedError(ctx)

@InstructionRegistry.register
class SIZE(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RLL.RungStatus:
            dim = self.args[1]
            source , dims = splitArrayPath(self.args[0])
            source = self.getMemory(source)
            
            dim = getPLCValue(self.getMemory(self.args[1]))
            dest:DataVariant = self.getMemory(self.args[2])

            if not isinstance(source, (Array | STRING)):
                self.raiseNotImplementedError(ctx)

            if isinstance(source, STRING):
                size = source._maxlength
            else:
                match dim:
                    case 0:
                        size = len(source)
                    case 1:
                        size = len(source[0])
                    case 2:
                        size = len(source[0][0])
                    case _:
                        raise ValueError(f"{__class__} dim value out of range {dim}")

            dest.setValue(size)