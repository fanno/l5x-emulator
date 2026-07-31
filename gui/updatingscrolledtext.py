import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

from gui.helper import getParentTab

class UpdatingScrolledText(ScrolledText):
    def __init__(self, master, name:str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.name = name
        self.pack(fill=tk.BOTH, expand=tk.TRUE)
        
        self._notebook, self._tab_id = getParentTab(self)

    def canUpdate(self) -> bool:
        _, pos = self.yview()
        pos = float(pos)
        selected = bool(self.tag_ranges('sel'))
        return self.focus_get() != self or (not selected and pos >= 1.0)
    
    def updateContent(self) -> bool:
        canUpdate = self.canUpdate()
        if self.canUpdate():
            self.setTabTitle(f"{self.name} ▶️")
        else:
            self.setTabTitle(f"{self.name} ⏸️")
        return canUpdate
    
    def setTabTitle(self, new_title):
        if isinstance(self._notebook, ttk.Notebook):
            self._notebook.tab(self._tab_id, text=new_title)
            return True
        return False