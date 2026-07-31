from contextlib import contextmanager

import engine.context

class Scan:
    Context:"engine.context.EmulatorContext" = None

class PreScan(Scan):
    _stack: list[int] = []
    
    @classmethod
    @contextmanager
    def scope(cls, ctx:"engine.context.EmulatorContext"):
        if cls.Context is None:
            cls.Context = ctx
        if cls.Context is None:
            yield
            return
        if not cls.Context.preScan:
            yield
            return

        cls._stack.append(hash(id(ctx)))
        try:
            yield
        finally:
            cls._stack.pop()
    
    @classmethod
    def isActive(cls) -> bool:
        if cls.Context:
            if cls.Context.preScan:
                return len(cls._stack) == 0
        return False

class PostScan(Scan):
    _stack: list[int] = []

    @classmethod
    @contextmanager
    def scope(cls, ctx:"engine.context.EmulatorContext"):
        if cls.Context is None:
            cls.Context = ctx
        if cls.Context is None:
            yield
            return
        if not cls.Context.postScan:
            yield
            return

        cls._stack.append(hash(id(ctx)))
        try:
            yield
        finally:
            cls._stack.pop()
    
    @classmethod
    def isActive(cls) -> bool:
        if cls.Context:
            if cls.Context.postScan:
                return len(cls._stack) == 0
        return False