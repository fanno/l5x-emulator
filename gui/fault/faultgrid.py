import logging

from tkinter.ttk import Treeview, Scrollbar
from tkinter import Event, PhotoImage
import tkinter as tk

from engine.errors import PLCFault

import json
from collections import defaultdict

class FaultGrid(Treeview):
    PADDING = 5
    ENTRY_WIDTH = 20

    _edit_entry: tk.Entry = None

    skipUpdate:float

    FAULT_TEXTS = defaultdict(dict)

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.checked_img = PhotoImage(width=16, height=16)
        self.checked_img.put("green", to=(0,0,15,15))
        
        self.unchecked_img = PhotoImage(width=16, height=16)
        self.unchecked_img.put("gray", to=(0,0,15,15))
        
        self.skipUpdate = 0.0

        self["columns"]=('time', 'type', 'code', 'location', 'desc')
        
        self.heading('#0', text='#')
        self.heading('time', text='Time')
        self.heading('type', text='Type')
        self.heading('code', text='Code')
        self.heading('location', text='Location')
        self.heading('desc', text='Description')
        self.column('#0', anchor='w', minwidth=0, width=35, stretch=tk.NO)
        self.column('time', anchor='w', width=120, stretch=tk.NO)
        self.column('type', anchor='center', width=40, stretch=tk.NO)
        self.column('location', anchor='w', width=250, stretch=tk.NO)
        self.column('code', anchor='center', width=40, stretch=tk.NO)
        self.column('desc', anchor='w')

        v_scroll = Scrollbar(self, orient=tk.VERTICAL, command=self._on_scroll)
        v_scroll.grid(row=0, column=1, sticky=tk.NS)
        self.configure(yscrollcommand=v_scroll.set, takefocus=0)

        self.tag_configure('even', background='#FFFFFF', foreground='black')
        self.tag_configure('odd',  background='#F0F0F0', foreground='black')
        self.grid(row=0, column=0, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.bind('<MouseWheel>', self._on_mousewheel)

        FaultGrid.loadText()

        self.pack(fill=tk.BOTH, expand=tk.TRUE)

    def _on_scroll(self, *args):
        self.yview(*args)

    def _on_mousewheel(self, event:Event):
        if event.num == 4:
            delta = -5
        elif event.num == 5:
            delta = 5
        else:
            delta = -5 if event.delta > 0 else 5

        self.yview_scroll(delta, tk.UNITS)
        return 'break'

    def updateContent(self, data:list[PLCFault]):
        if self.winfo_viewable():
            self.delete(*self.get_children())

            for k, v in enumerate(data):
                value = (str(v.time), str(v.type), str(v.code), v.path, FaultGrid.getText(v.type, v.code))
                tag = 'odd' if k % 2 else 'even'
                tags=(tag,)
                iid = self.insert('', tk.END, text=str(k), values=value, open=tk.FALSE,tags=tags)

    def _populate(self, parent, data:list[PLCFault]):
        for k, v in enumerate(data):
            value = (str(v.time), str(v.type), str(v.code), FaultGrid.getText(v.type, v.code))
            tag = 'odd' if k % 2 else 'even'
            tags=(tag,)
            iid = self.insert(parent, tk.END, text=str(k), values=value, open=tk.FALSE,tags=tags)

    @staticmethod
    def loadText():
        if not FaultGrid.FAULT_TEXTS:
            try:
                with open("errorcodes.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                for item in data:
                    FaultGrid.FAULT_TEXTS[item["Type"]][item["Code"]] = item["Text"]
            except Exception as e:
                logging.error(e)

    @staticmethod
    def getText(type:int, code:int) -> str:
        type_dict = FaultGrid.FAULT_TEXTS.get(type)

        if type_dict is None:
            return f"Unknown fault (Type={type}, Code={code})"

        return type_dict.get(
            code,
            f"Unknown fault (Type={type}, Code={code})"
        )
