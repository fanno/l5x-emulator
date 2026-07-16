from xml.etree import ElementTree

from typing import Any

class CoreException(Exception):
    pass

class UnhandeledTag(CoreException):
    def __init__(self, key:str, value:str, element:ElementTree):
        super().__init__(f"UnhandeledTag: {key}, {value}")
        self.key = key
        self.value = value
        self.element = element

class ParseTagException(CoreException):
    def __init__(self, name:str, element:ElementTree):
        super().__init__(f"Parse Structure  Tag: {name}, {element}")
        self.name = name
        self.element = element

class MemoryException(CoreException):
    def __init__(self, text:str , path:str, value:Any=None):
        super().__init__(f"{text}: {path}, {value}")
        self.path = path
        self.value = value