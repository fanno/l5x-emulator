import weakref
import threading
import logging
from typing import Callable, Dict, List, Any, Optional, Type
from uuid import uuid4

def subscribe_event(*event_classes: Type):
    def decorator(func):
        func._event_listener = True
        func._event_classes = event_classes if event_classes else None
        return func
    return decorator

class EventBus:
    _instance: Optional['EventBus'] = None
    _lock = threading.Lock()

    _handlers: Dict[Type, List[tuple]] = {}
    _wildcard_handlers: List[tuple] = []

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._handlers = {}
                    cls._instance._wildcard_handlers = []
        return cls._instance

    @classmethod
    def get(cls) -> 'EventBus':
        return cls()

    @classmethod
    def reset(cls):
        with cls._lock:
            if cls._instance:
                cls._instance._handlers.clear()
                cls._instance._wildcard_handlers.clear()
                cls._instance = None

    def _normalize_handler(self, handler: Callable) -> Callable:
        if isinstance(handler, weakref.WeakMethod):
            return handler
        if hasattr(handler, '__self__') and callable(handler):
            return weakref.WeakMethod(handler)
        return handler

    def _id(self) -> str:
        return str(uuid4())

    def subscribe(self, event_class: Type, handler: Callable[[Any], None]) -> str:
        sub_id = self._id()
        with self._lock:
            if event_class not in self._handlers:
                self._handlers[event_class] = []
            self._handlers[event_class].append((sub_id, self._normalize_handler(handler)))
        return sub_id

    def subscribe_wildcard(self, handler: Callable[[Any], None]) -> str:
        sub_id = self._id()
        with self._lock:
            self._wildcard_handlers.append((sub_id, self._normalize_handler(handler)))
        return sub_id

    def unsubscribe(self, sub_id: str):
        with self._lock:
            for event_class, handlers in list(self._handlers.items()):
                self._handlers[event_class] = [
                    (sid, h) for sid, h in handlers if sid != sub_id
                ]
                if not self._handlers[event_class]:
                    del self._handlers[event_class]
            self._wildcard_handlers = [
                (sid, h) for sid, h in self._wildcard_handlers if sid != sub_id
            ]

    def dispatch(self, event_instance: Any):
        event_type = type(event_instance)
        
        with self._lock:
            specific_handlers = self._handlers.get(event_type, [])[:]
            wildcard_handlers = self._wildcard_handlers[:]

        seen_ids = set()
        all_calls = []

        for sub_id, handler in specific_handlers:
            if sub_id not in seen_ids:
                all_calls.append(handler)
                seen_ids.add(sub_id)
        
        for sub_id, handler in wildcard_handlers:
            if sub_id not in seen_ids:
                all_calls.append(handler)
                seen_ids.add(sub_id)

        for handler in all_calls:
            try:
                bound_method = handler()
                if bound_method is not None:
                    bound_method(event_instance)
            except Exception as e:
                logging.exception(f"Error in handler for {event_type.__name__}: {e}")

    def cleanup_dead_references(self):
        with self._lock:
            for event_class, handlers in list(self._handlers.items()):
                self._handlers[event_class] = [
                    (sid, h) for sid, h in handlers 
                    if not isinstance(h, weakref.WeakMethod) or h() is not None
                ]
                if not self._handlers[event_class]:
                    del self._handlers[event_class]
            self._wildcard_handlers = [
                (sid, h) for sid, h in self._wildcard_handlers
                if not isinstance(h, weakref.WeakMethod) or h() is not None
            ]

class EventListener:
    def __init__(self):
        super().__init__()

        self._event_bus = EventBus.get()
        self._subscriptions: List[str] = []
        self._register_listeners()

    def _register_listeners(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_event_listener'):
                event_classes = attr._event_classes

                if event_classes is None:
                    sub_id = self._event_bus.subscribe_wildcard(attr)
                else:
                    for ec in event_classes:
                        sub_id = self._event_bus.subscribe(ec, attr)
                self._subscriptions.append(sub_id)

    def unregister_all(self):
        for sub_id in self._subscriptions:
            self._event_bus.unsubscribe(sub_id)
        self._subscriptions.clear()

    def __del__(self):
        self.unregister_all()