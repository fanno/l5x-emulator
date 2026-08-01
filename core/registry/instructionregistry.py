import logging

from typing import TypeVar, Dict, ClassVar, TYPE_CHECKING

import engine.context

if TYPE_CHECKING:   
    from engine.instruction import Instruction

TT = TypeVar("TT", bound=type)

class InstructionRegistry:
    _global_registry: ClassVar[Dict[str, "Instruction"]] = {}
    _local_registry: ClassVar[Dict[str, "Instruction"]] = {}

    @staticmethod
    def register(cls: TT, n:str = None) -> TT:
        if n:
            name = n
        else:
            name = cls.__name__

        name = name.upper()
        if name in InstructionRegistry._global_registry:
            raise ValueError(f"Instruction global, {name} already registered")
        InstructionRegistry._global_registry[name] = cls
        return cls

    @staticmethod
    def register_local(cls: TT, n:str = None) -> TT:
        if n:
            name = n
        else:
            name = cls.__name__

        name = name.upper()
        if name in InstructionRegistry._local_registry:
            raise ValueError(f"Instruction local, {name} already registered")
        InstructionRegistry._local_registry[name] = cls
        return cls    

    @staticmethod
    async def execute(name:str, args:list[str], ctx:"engine.context.ExecutionContext") -> None:
        name = name.upper()
        if name not in InstructionRegistry._global_registry:
            raise KeyError(f"Instruction {name} not supported")
        
        from engine.instruction import Instruction
        cls = InstructionRegistry._global_registry[name]
        if isinstance(cls, Instruction):
            from engine.routine import RoutineType
            logging.debug(f"InstructionRegistry: {name}> {args}, {ctx}")
            match ctx.Type:
                case RoutineType.RLL:
                    await cls.ladder(args, ctx)
                case RoutineType.ST:
                    await cls.st(args, ctx)
                case RoutineType.FBD:
                    ## TODO not aplickable ?
                    #await cls.fbd(args, ctx)
                    pass
                case RoutineType.SFC:
                    await cls.sfc_execute(args, ctx)
        else:
            logging.error(f"InstructionRegistry: {name}> {args}, {ctx}")

    @staticmethod
    def get(name:str) -> "Instruction":
        name = name.upper()
        if name in InstructionRegistry._global_registry:
            return InstructionRegistry._global_registry[name]
        if name in InstructionRegistry._local_registry:
            return InstructionRegistry._local_registry[name]
        raise KeyError(f"Instruction {name} not found")

    @staticmethod
    def has(name:str) -> bool:
        name = name.upper()
        return name in InstructionRegistry._global_registry or name in InstructionRegistry._local_registry

    @staticmethod
    def clear_local() -> None:
        InstructionRegistry._local_registry = {}