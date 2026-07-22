import logging

from typing import TypeVar, Dict, ClassVar, TYPE_CHECKING

import engine.context

if TYPE_CHECKING:   
    from engine.instruction import Instruction

TT = TypeVar("TT", bound=type)

class InstructionRegistry:
    _registry: ClassVar[Dict[str, "Instruction"]] = {}

    @staticmethod
    def register(cls: TT, n:str = None) -> TT:
        if n:
            name = n
        else:
            name = cls.__name__

        name = name.upper()
        if name in InstructionRegistry._registry:
            raise ValueError(f"Instruction {name} already registered")
        InstructionRegistry._registry[name] = cls
        return cls

    @staticmethod
    async def execute(name:str, args:list[str], ctx:"engine.context.ExecutionContext") -> None:
        name = name.upper()
        if name not in InstructionRegistry._registry:
            raise KeyError(f"Instruction {name} not supported")
        
        from engine.instruction import Instruction
        cls = InstructionRegistry._registry[name]
        if isinstance(cls, Instruction):
            from engine.routine import RoutineType
            logging.debug(f"InstructionRegistry: {name}> {args}, {ctx}")
            match ctx.Type:
                case RoutineType.RLL:
                    await cls.ladder_execute(args, ctx)
                case RoutineType.ST:
                    await cls.st_execute(args, ctx)
                case RoutineType.FBD:
                    await cls.fbd_execute(args, ctx)
                case RoutineType.SFC:
                    await cls.sfc_execute(args, ctx)
        else:
            logging.error(f"InstructionRegistry: {name}> {args}, {ctx}")

    @staticmethod
    def get(name:str) -> "Instruction":
        name = name.upper()
        if name not in InstructionRegistry._registry:
            raise KeyError(f"Instruction {name} not supported")
        
        return InstructionRegistry._registry[name]

    @staticmethod
    def has(name:str) -> bool:
        name = name.upper()
        return name in InstructionRegistry._registry