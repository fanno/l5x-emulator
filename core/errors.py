from lxml.etree import _ElementTree as ElementTree

from typing import Any

class CoreException(Exception):
    hierarchy = ''
    def __init__(self, message):
        from engine.hierarchy import Hierarchy
        self.hierarchy = Hierarchy.path()
        super().__init__(f"{message}, ({self.hierarchy})")

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
        self.path = path
        self.value = value

        super().__init__(f"{text}: {self.path}, {self.value}")

class TNDException(CoreException):
    def __init__(self, text:str , path:str, value:Any=None):
        self.path = path
        self.value = value

        super().__init__(f"{text}: {self.path}, {self.value}")