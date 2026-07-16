from xml.etree.ElementTree import Element

from typing import Dict

from  engine.task import Task

def loadTasks(controller:Element, tasks:Dict[str, Task]):
    for task in controller.findall("./Tasks//Task"):
        p = Task(_Element=task)
        tasks[p.Name] = p