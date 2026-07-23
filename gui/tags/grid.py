import logging

from tkinter.ttk import Treeview, Scrollbar
from tkinter import Event, PhotoImage, Entry, END
import tkinter as tk

from typing import Any, Optional

from dataclasses import is_dataclass, fields, dataclass, field

import time

from numbers import Number

from utils.biindexmap import BiIndexMap

from datatypes.custom.string import STRING
from datatypes.custom.datavariant import DataVariant
from datatypes.custom.numbers import INTIGER, REAL
from datatypes.custom.bool import BOOL
from datatypes.custom.array import Array
from datatypes.custom.dt import DT

from collections.abc import Mapping, Sequence, Set


from eventbus.eventbus import EventBus
from core.events import UpdateVariableEvent

@dataclass
class DataPair:
    PATH:str = field(init=True)
    IID:str = field(init=True)
    DATA:Any = field(init=True)

    def __post_init__(self):
        if isinstance(self.PATH, (list, tuple)):
            path = []
            for part in self.PATH:
                if isinstance(part, int):
                    part = str(part)
                path.append(part)
            self.PATH = ".".join(path)

class MappingData(BiIndexMap[DataPair]):
    def __init__(self):
        super().__init__(
            key1_func=lambda s: s.PATH,
            key2_func=lambda s: s.IID,
            expected_type=DataPair
        )

    def getByPath(self, path: str) -> Optional[DataPair]:
        return self._get_by_first(path)

    def getById(self, id: str) -> Optional[DataPair]:
        return self._get_by_second(id)

class Grid(Treeview):
    PADDING = 5
    ENTRY_WIDTH = 20

    createUI:bool

    container:str = None

    _edit_entry: Entry = None

    rawData = None

    skipUpdate:float

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.checked_img = PhotoImage(width=16, height=16)
        self.checked_img.put("green", to=(0,0,15,15))
        
        self.unchecked_img = PhotoImage(width=16, height=16)
        self.unchecked_img.put("gray", to=(0,0,15,15))

        self.data = MappingData()
        
        self.createUI = True
        self.skipUpdate = 0.0

        self.heading('#0', text='Name')
        self.heading('type', text='Type')
        self.heading('value', text='Value')
        self.column('#0', anchor='w', width=150)
        self.column('type', anchor='center', width=80)
        self.column('value', anchor='w', width=120)

        v_scroll = Scrollbar(self, orient=tk.VERTICAL, command=self._on_scroll)
        v_scroll.grid(row=0, column=1, sticky=tk.NS)
        self.configure(yscrollcommand=v_scroll.set, takefocus=0)

        self.tag_configure('even', background='#FFFFFF', foreground='black')
        self.tag_configure('odd',  background='#F0F0F0', foreground='black')

        self.grid(row=0, column=0, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.bind("<Button-1>", self._on_click)
        self.bind('<MouseWheel>', self._on_mousewheel)
        self.bind("<<TreeviewOpen>>", lambda e: self.after(1, self._update_stripes))
        self.bind("<<TreeviewClose>>", lambda e: self.after(1, self._update_stripes))

        self.updateTask()

    def _update_stripes(self, event:Event=None):
        index = 0
        def walk(parent_id):
            nonlocal index

            children = self.get_children(parent_id)
            for child in children:
                tag = 'odd' if index % 2 else 'even'
                self.item(child, tags=(tag,))
                index += 1
                if self.item(child, 'open'):
                    walk(child)
        walk("")

    def hideEdit(self) -> bool:
        self.skipUpdate = time.monotonic()
        if self._edit_entry:
            self._edit_entry.destroy()
            self._edit_entry = None
            return True
        return False

    def _on_scroll(self, *args):
        self.hideEdit()
        self.yview(*args)

    def updateData(self, container:str, data):
        self.container = container

        self.rawData = data

        if self.createUI:
            self.delete(*self.get_children())
            self._populate(parent='', data=self.rawData, path=[])
            self._update_stripes()
        self.createUI = False

    def updateTask(self, event:Event = None):
        if time.monotonic() > self.skipUpdate+1:
            if self.rawData and not self.createUI and self.winfo_viewable():
                self._populate(parent='', data=self.rawData, path=[])

                self._update_stripes()
            self.after(1000, self.updateTask)
        else:
            self.after(100, self.updateTask)

    def _on_mousewheel(self, event:Event):
        self.hideEdit()

        if event.num == 4:
            delta = -5
        elif event.num == 5:
            delta = 5
        else:
            delta = -5 if event.delta > 0 else 5

        self.yview_scroll(delta, tk.UNITS)
        return 'break'

    def _populate(self, parent, data, path):
        if is_dataclass(data):
            if isinstance(data, Array):
                for k, v in enumerate(data):
                    self._populateRow(parent, str(k), v, path)
            elif not isinstance(data, (INTIGER, REAL, BOOL)):
                for f in fields(data):
                    if f.repr:
                        k = f.name
                        v = getattr(data, k)
                        self._populateRow(parent, k, v, path)
        else:
            if isinstance(data, dict):
                for k, v in data.items():
                    self._populateRow(parent, k, v, path)           

    def _populateRow(self, parent, key, value, path):
        cur_path = path + [key]

        isObject = self.isObjectLike(value)

        if self.createUI:
            iid = self.insert(parent, tk.END, text=key, values=self.getRowValue(value), open=tk.FALSE)

            display = self._populateTypeRow(parent=iid, data=value, path=cur_path)
            if display and isObject:
                self._populate(parent=iid, data=value, path=cur_path)

            self.setItem(iid, value, path=cur_path)
        else:
            display = self._populateTypeRow(parent=None, data=value, path=cur_path)
            if display and isObject:
                data = self.data.getByPath(cur_path)
                if self.item(data.IID, "open"):
                    self._populate(parent=None, data=value, path=cur_path)

            data = self.data.getByPath(cur_path)
            if data:
                self.setItem(data.IID, value)

    def isVisible(self, iid):

        self.i
        idx = self.index(iid)

        total = len(self.get_children(""))

        if total == 0:
            return False

        top_frac, bottom_frac = self.yview()
        
        if top_frac == 0.0 and (bottom_frac == 1.0 or bottom_frac == 0.0):
            return True
        
        row_frac = idx / total

        margin = 0.01

        return (top_frac - margin) <= row_frac <= (bottom_frac + margin)
        return bool(self.bbox(iid))

    def _populateTypeRow(self, parent, data, path) -> bool:
        if isinstance(data, STRING):
            self._populate(parent, {'LEN': data.LEN}, path)
            self._populate(parent, {'DATA': data.DATA}, path)
            return False
        if isinstance(data, DT):
            return False
        return True

    def getRowValue(self, value):
        if isinstance(value, (STRING, DT)):
            return (value.__class__.__name__, value.toString())
        elif isinstance(value, Array):
            return (value.getType(), '')
        elif isinstance(value, (DataVariant)):
            return (value.__class__.__name__, value.getPLCValue())
        elif (not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, bool)):
            return (value.__class__.__name__, '')
        
        return (value.__class__.__name__, value)

    def setItem(self, iid, rawValue, path=None, send=False):
        if path:
            self.data.add(DataPair(PATH=path,
                                   IID=iid,
                                   DATA=rawValue))

        if self.isVisible(iid) or send or path:
            variable = self.data.getById(iid)

            if variable:
                if variable.DATA == rawValue and not send and not path:
                    return
                try:
                    if type(variable.DATA) == type(rawValue):
                        variable.DATA = rawValue
                    elif isinstance(variable.DATA, DataVariant) and not isinstance(rawValue, DataVariant):
                        variable.DATA.setValue(rawValue)
                    else:
                        variable.DATA = rawValue

                    if send:
                        self._item_changed(iid)

                    value = self.getRowValue(variable.DATA)

                    if isinstance(value[1], bool):
                        img = self.checked_img if value[1] else self.unchecked_img

                        self.item(iid, image=img, values=value)
                    else:
                        self.item(iid, values=value)
                except Exception as e:
                    logging.error(e)

    def _on_click(self, event:Event):
        hidden = self.hideEdit()
        if not hidden:
            region = self.identify_region(event.x, event.y)
            column = self.identify_column(event.x)
            editable = (region == "cell" and column == "#2")
            if region == "tree" or editable:
                iid = self.identify_row(event.y)
                if iid:
                    data = self.data.getById(iid)
                    if data:
                        if isinstance(data.DATA, BOOL):
                            self.setItem(iid, not data.DATA.getPLCValue(), send=True)
                        elif editable:
                            if isinstance(data.DATA, (DataVariant)):
                                self.edit_cell(iid, column)

    def init_edit_cell(self, iid, column):
        x, y, width, height = self.bbox(iid, column)

        edit = Entry(self)
        edit.place(x=x, y=y, width=width, height=height)

        values = self.item(iid, "values")
        current_text = values[1]

        if not current_text: current_text = ""

        edit.insert(0, current_text)
        edit.select_range(0, tk.END)
        edit.focus()
        return edit

    def edit_cell(self, iid, column):
        if self._edit_entry is None:
            self._edit_entry = self.init_edit_cell(iid, column)

            def save(event=None):
                new_text = self._edit_entry.get()

                data = self.data.getById(iid)
                if data:
                    old_value = data.DATA
                    if isinstance(old_value, DataVariant):
                        old_value = self.getRowValue(old_value)

                    try:
                        if isinstance(old_value, int):
                            new_val = int(new_text.strip())
                        elif isinstance(old_value, float):
                            new_val = float(new_text.strip())
                        else:
                            new_val = new_text
                    except ValueError:
                        new_val = old_value
                    
                    self.setItem(iid, new_val, send=True)

                self.hideEdit()

            self._edit_entry.bind("<Return>", save)
            self._edit_entry.bind("<FocusOut>", lambda e: self.hideEdit())

    def _item_changed(self, iid):
            data = self.data.getById(iid)
            if data:
                EventBus.get().dispatch(UpdateVariableEvent(self.container,
                                                        data.PATH,
                                                        data.DATA))

    def isObjectLike(self, value):
        if isinstance(value, (bool, int, float, complex)):
            return False
        if isinstance(value, (Mapping, Sequence, Set)):
            if isinstance(value, (str, bytes, bytearray)):
                return False
            return True
        if hasattr(value, "__dict__"):
            return True
        if isinstance(value, Number):
            return False
        return True