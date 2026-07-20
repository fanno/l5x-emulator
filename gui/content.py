import tkinter as tk
from tkinter.ttk import Notebook, Frame

from gui.tags.grid import Grid
from gui.tags.tags import TagsTabs
from gui.status import StatusText
from core.events import StatusEvent
from gui.log import LogText, Logger

class ContentTabs(Notebook):
    tabs:dict[str, Grid]

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        titel = "PLC Tags"
        frame = Frame(self)
        self.add(frame, text=titel)
        self.tagsTabs = TagsTabs(frame)

        titel = "PLC Status"
        frame = Frame(self)
        self.add(frame, text=titel)
        self.status = StatusText(frame, name=titel)
        
        titel = "Error Log"
        frame = Frame(self)
        self.add(frame, text=titel)
        self.log = LogText(frame, titel)

        self.pack(fill=tk.BOTH, expand=tk.TRUE)

    def updateContent(self, status:StatusEvent, logger:Logger):
        if status.Tags:
            self.tagsTabs.updateTags(status.Tags)
        self.status.updateContent(status)
        self.log.updateContent(logger)