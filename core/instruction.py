from engine.context import ExecutionContext

class Instruction:

    @staticmethod
    async def execute(args:list[str], ctx:"ExecutionContext") -> None:
        raise NotImplementedError(f"{__class__} not implemented yet")