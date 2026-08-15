import logging
import time

import tkinter as tk
from tkinter.ttk import Treeview, Scrollbar
from tkinter import Event, PhotoImage

from typing import Optional

from dataclasses import dataclass, field

from utils.indexmap import IndexMap

from datatypes.custom.array import Array
from datatypes.custom.dt import DT

from eventbus.eventbus import EventBus
from core.events import UpdateVariableEvent, StatusRequestEvent
from core.registry.datatyperegistry import DataTypeRegistry

from protocols.memory import SupportsGetPLCValue, SupportsToString

from utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryObject, DT, UIMemoryPrimitive, MemoryType

@dataclass
class DataPair:
    PATH:str = field(init=True)
    IID:str = field(init=True)
    DATA:MemoryType = field(init=True)

    def __post_init__(self):
        if isinstance(self.PATH, (list, tuple)):
            path = []
            for part in self.PATH:
                if isinstance(part, int):
                    part = str(part)
                path.append(part)
            self.PATH = ".".join(path)

class MappingData(IndexMap[DataPair]):
    def __init__(self):
        super().__init__(expected_type=DataPair)

        self.IDX_PATH = self._addIndex(lambda s: s.PATH)
        self.IDX_IID = self._addIndex(lambda s: s.IID)

    def getByPath(self, path: str) -> Optional[DataPair]:
        return self.get(self.IDX_PATH, path)

    def getById(self, id: str) -> Optional[DataPair]:
        return self.get(self.IDX_IID, id)

class Grid(Treeview):
    PADDING = 5
    ENTRY_WIDTH = 20

    createUI:bool

    Container:str = None

    _edit_entry: tk.Entry = None

    rawData = None

    skipUpdate:float

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.checked_img = PhotoImage(width=16, height=16)
        self.checked_img.put("green", to=(0,0,15,15))
        
        self.unchecked_img = PhotoImage(width=16, height=16)
        self.unchecked_img.put("gray", to=(0,0,15,15))

        self.mapping = MappingData()
        
        self.skipUpdate = 0.0
        self.Container = None

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

        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.bind("<Button-1>", self._on_click)
        self.bind('<MouseWheel>', self._on_mousewheel)
        self.bind("<<TreeviewOpen>>", lambda e: self.after(1, self._on_view_changed))
        self.bind("<<TreeviewClose>>", lambda e: self.after(1, self._on_view_changed))

        self.bind("<Configure>", self._on_view_changed)

        self.updateTask()

    def _update_stripes(self, event:Event=None):
        self._on_view_changed()

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
        self._on_view_changed()

    def updateData(self, Container:str, data):
        self.visible_iids = self.get_visible_items()
        
        self.rawData = data
        if self.Container != Container:
            self.delete(*self.get_children())
            self._populate(parent='', data=self.rawData[Container], path=[], create=True)
            self._update_stripes()
        self.Container = Container

    def updateTask(self, event:Event = None):
        if time.monotonic() > self.skipUpdate+1:
            if self.rawData and self.winfo_viewable():
                if self.Container:
                    if self.Container in self.rawData:
                        self._populate(parent='', data=self.rawData[self.Container], path=[])

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
        self._on_view_changed()
        return 'break'

    def _populate(self, parent:str, data:MemoryType|dict, path:list, create:bool=False):
        if isinstance(data, MemoryType):
            if isinstance (data, UIMemoryObject):
                for k, v in data.Value.items():
                    self._populateRow(parent=parent, key=k, value=v, path=path, create=create)
        else:
            if isinstance(data, dict):
                for k, v in data.items():
                    self._populateRow(parent=parent, key=k, value=v, path=path, create=create)

    def _populateRow(self, parent:str, key:str, value:MemoryType, path:list, create:bool=False):
        cur_path = path + [key]

        isObject = self.isObjectLike(value)

        if create:
            iid = self.insert(parent, tk.END, text=key, values=self.getRowValue(value), open=tk.FALSE)

            display = self._populateTypeRow(parent=iid, data=value, path=cur_path)
            if display and isObject:
                
                self._populate(parent=iid, data=value, path=cur_path, create=create)

            self.setItem(iid, rawValue=value, path=cur_path)
        else:
            data = self.mapping.getByPath(cur_path)
            if data:
                display = self._populateTypeRow(parent=None, data=value, path=cur_path)
                if display and isObject:
                    if self.item(data.IID, "open"):
                        self._populate(parent=None, data=value, path=cur_path)

                self.setItem(data.IID, rawValue=value)

    def _on_view_changed(self, event:Event=None):
        self.visible_iids = self.get_visible_items()

        paths:list[str] = []

        for index, iid in enumerate(self.visible_iids):
            tag = "odd" if index % 2 else "even"
            self.item(iid, tags=(tag,))

            data = self.mapping.getById(iid)
            if data:
                paths.append(data.PATH)

        event = StatusRequestEvent(Container=self.Container, Paths=paths)
        EventBus.get().dispatch(event)

    def get_visible_items(self):
        visible = []
        viewport_height = self.winfo_height()

        y = 0
        first = None

        while y < viewport_height:
            first = self.identify_row(y)
            if first and self.bbox(first):
                break
            y += 5

        if not first:
            return visible

        bbox = self.bbox(first)
        if not bbox:
            return visible

        row_height = bbox[3]

        for y in range(0, viewport_height + row_height, row_height):
            iid = self.identify_row(y)

            if iid:
                visible.append(iid)
        return visible

    def isVisible(self, iid):
        return iid in self.visible_iids

    def _populateTypeRow(self, parent, data:UIMemoryPrimitive, path) -> bool:
        if isinstance(data, UIMemoryPrimitive):
            if data.Datatype == DT.STRING:
                return True
                self._populate(parent, {'LEN': data.LEN}, path)
                self._populate(parent, {'DATA': data.DATA}, path)
                return False
            if isinstance(data, DT):
                return False
            return True
        else:
            return True

    def getRowValue(self, value:MemoryType):
        if isinstance(value, UIMemoryPrimitive):
            return (value.Datatype.value, value.Value)
        if isinstance(value, UIMemoryObject):
            if value.Class:
                return (value.Class, "")
            else:
                return (value.Datatype.value, "")
        return ("", "")

        if isPLCInstance(value, SupportsToString):
            return (value.__class__.__name__, value.toString())
        elif isinstance(value, Array):
            return (value.getType(), '')
        elif isPLCInstance(value, (SupportsGetPLCValue)):
            return (value.__class__.__name__, value.getPLCValue())
        elif (not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, bool)):
            return (value.__class__.__name__, '')
        
        return (value.Datatype.value, value.Value)

    def setItem(self, iid, rawValue:MemoryType=None, editValue=None, path=None, send=False):
        if rawValue is None and editValue is None:
            return

        if path and rawValue:
            self.mapping.add(DataPair(PATH=path,
                                   IID=iid,
                                   DATA=rawValue))
        if self.isVisible(iid) or send or path:
            variable = self.mapping.getById(iid)

            if variable:
                
                if (rawValue is not None and variable.DATA.Value == rawValue.Value) or (editValue is not None and variable.DATA.Value == editValue):
                    if not send and not path:
                        return
               
                try:
                    if rawValue is not None:
                        variable.DATA = rawValue
                    else:
                        cls = DataTypeRegistry.get(variable.DATA.Datatype.value)
                        val = cls(editValue)
                        if isPLCInstance(val, SupportsGetPLCValue):
                            variable.DATA.Value = val.getPLCValue()

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
                    data = self.mapping.getById(iid)
                    if data:
                        if isinstance(data.DATA.Value, bool):
                            self.setItem(iid, editValue=not data.DATA.Value, send=True)
                        elif editable:
                            if isinstance(data.DATA, UIMemoryPrimitive):
                                self.edit_cell(iid, column)

    def init_edit_cell(self, iid, column):
        x, y, width, height = self.bbox(iid, column)

        edit = tk.Entry(self)
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

                data = self.mapping.getById(iid)
                if data:
                    if isinstance(data.DATA, UIMemoryPrimitive):
                        try:
                            if isinstance(data.DATA.Value, int):
                                new_val = int(new_text.strip())
                            elif isinstance(data.DATA.Value, float):
                                new_val = float(new_text.strip())
                            else:
                                new_val = new_text
                        except ValueError:
                            new_val = data.DATA.Value

                        self.setItem(iid, editValue=new_val, send=True)

                self.hideEdit()

            self._edit_entry.bind("<Return>", save)
            self._edit_entry.bind("<FocusOut>", lambda e: self.hideEdit())

    def _item_changed(self, iid):
            data = self.mapping.getById(iid)
            if data:
                EventBus.get().dispatch(UpdateVariableEvent(self.Container,
                                                            data.PATH,
                                                            data.DATA.Value))

    def isObjectLike(self, value):
        if isinstance(value, UIMemoryPrimitive):
            if value.Datatype == DT.STRING:
                return True
            return False
        return True