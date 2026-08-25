from tkinter.ttk import Frame, Label, Combobox
import tkinter as tk

from core.memory.memory import Memory

from gui.tags.grid import Grid

class TagsTabs(Frame):
    tabs:dict[str, Grid]

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tabs = {}
        self.pack(fill=tk.BOTH, expand=True)

        control_frame = Frame(self)
        control_frame.pack(fill=tk.X, padx="5", pady="5")
        
        Label(control_frame, text="Tag:").pack(side=tk.LEFT)

        self.current_tab = None

        self.tag_dropdown = Combobox(
            control_frame,
            state="readonly",
            width=30
        )
        self.tag_dropdown.pack(side=tk.LEFT, padx=(5, 0))
        self.tag_dropdown.bind("<<ComboboxSelected>>", self.on_tag_change)
        
        self.tree_container = Frame(self)
        self.tree_container.pack(fill=tk.BOTH, expand=True, padx="5", pady="5")

        self.treeview = None

        self.data = {}


    def deep_merge(self, base: dict, override: dict) -> dict:
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self.deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def  updateTags(self, data: dict[str, Memory]):
        self.data = self.deep_merge(self.data or {}, data)
        '''
        if not self.data:
            self.data = data
        else:
            self.data.update(data)
            #for key, value in data.items():
            #    self.data[key] = value
        '''

        tag_names = list(self.data.keys())
        self.tag_dropdown['values'] = tag_names
        if not self.current_tab and tag_names:
            self.tag_dropdown.current(0)
            self.current_tab = tag_names[0]

        self._update()
    
    def on_tag_change(self, event=None):
        selected = self.tag_dropdown.get()
        
        if not selected or selected == self.current_tab:
            return
        
        self.current_tab = selected
        
        self.clearGrid()
        self._update()
    
    def _update(self):
        if self.treeview is None:
            self.treeview = Grid(
                self.tree_container,
                columns=('type', 'value'),
                show='tree headings',
                selectmode=tk.NONE
            )
            self.treeview.pack(fill=tk.BOTH, expand=True)

        if self.treeview:
            if isinstance(self.treeview, Grid):
                self.treeview.updateData(self.current_tab, self.data)

    def clearGrid(self):
        for widget in self.tree_container.winfo_children():
            widget.destroy()
        self.treeview = None