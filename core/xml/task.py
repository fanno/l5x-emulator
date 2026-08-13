from lxml.etree import _Element as Element

from typing import Dict

from  engine.task import Task

from core.events import LoadingEvent
from eventbus.eventbus import EventBus

def loadTasks(controller:Element, tasks:Dict[str, Task]):
    for task in controller.findall("./Tasks//Task"):
        p = Task(_Element=task)
        EventBus.get().dispatch(LoadingEvent(f"Task: {p.Name}"))
        tasks[p.Name] = p