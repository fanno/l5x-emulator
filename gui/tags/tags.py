from tkinter.ttk import Notebook

from core.memory.memory import Memory

from gui.tags.grid import Grid

class TagsTabs(Notebook):
    tabs:dict[str, Grid]

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tabs = {}

    def updateData(self, data:dict[str, Memory]):
        tab = None
        
        cur = self.select()
        for k,v in data.items():
            if isinstance(v, dict):
                force = False
                if k not in self.tabs:
                    force = True
                    tab = Grid(
                        self,
                        columns=('type', 'value'),
                        show='tree headings',
                        selectmode='none',
                        )

                    self.add(tab, text=k)

                    self.tabs[k] = tab

                if str(self.tabs[k]) == cur or force:
                    self.tabs[k].updateData(k, v)

        if tab is not None:
            self.pack(expand=True, fill="both")