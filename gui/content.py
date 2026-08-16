import tkinter as tk
from tkinter.ttk import Notebook, Frame

from gui.tags.grid import Grid
from gui.tags.tags import TagsTabs
from gui.fault.faults import FaultTabs

from gui.status import StatusText
from core.events import StatusEvent

class ContentTabs(Notebook):
    tabs:dict[str, Grid]

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        titel = "PLC Status"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.status = StatusText(frame, name=titel)

        titel = "PLC Tags"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.tagsTabs = TagsTabs(frame)

        titel = "Fault Logs"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.fault = FaultTabs(frame, titel)

        self.pack(fill=tk.BOTH, expand=tk.TRUE)

    def updateContent(self, status:StatusEvent):
        if status.Tags:
            self.tagsTabs.updateTags(status.Tags)
        self.status.updateContent(status)