import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

class UpdatingScrolledText(ScrolledText):
    def __init__(self, master, name:str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.name = name
        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        self._notebook = None

        widget = self.master
        while widget is not None:
            if isinstance(widget, ttk.Notebook):
                # Try each tab — find the one that contains us
                for tab_id in widget.tabs():
                    tab_widget = widget.nametowidget(tab_id)
                    # Check if we're inside this tab
                    w = self
                    while w is not None:
                        if w is tab_widget:
                            self._tab_id = tab_id
                            self._notebook = widget
                            break
                        w = w.master
                    if self._notebook:
                        break
            if self._notebook:
                break
            widget = widget.master

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