import psutil
import os
import tkinter as tk

from core.events import StatusEvent

from gui.updatingscrolledtext import UpdatingScrolledText

class StatusText(UpdatingScrolledText):
    _process:psutil.Process
    _peak:float

    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master,
            name=name,
            wrap="word",
            state="disabled",
            font=("Consolas", 9),
            height=10)
        
        self._process:psutil.Process = psutil.Process(os.getpid())
        self._peak = 0.0
        
        self.configure(state=tk.NORMAL)
        self.insert("1.0", "")
        self.configure(state=tk.DISABLED)

    def updateContent(self, status:StatusEvent):
        current:float = self._process.memory_info().rss / 1024 / 1024
        if current > self._peak:
            self._peak = current

        update = super().updateContent()
        if update and self.winfo_viewable():
            if status.Runing:
                text = f"------------------ Total scan ------------------\n"
                text += f"Time current (Sec): {status.Scan.Last:.4f} ({status.ScanDelayed:.4f})\n"
                text += f"Time longest (Sec): {status.Scan.Max:.4f}\n"
                text += f"Count (number of plc scan): {status.Scan.Count}\n"
                for tname, task in status.Tasks.items():
                    text += f"------------------ {tname} ------------------\n"
                    text += f"Time current (Sec): {task.Last:.4f}\n"
                    text += f"Time longest (Sec): {task.Max:.4f}\n"
                    text += f"Count (number of plc scan): {task.Count}\n"
                text += f"------------------------------------------------\n"
                text += f"Memory current (MB): {current:.2f}\n"
                text += f"Memory max (MB): {self._peak:.2f}\n"
            else:
                text = f"Initializing OPC UA server..."
            
            self.configure(state=tk.NORMAL)
            self.delete("1.0", tk.END)
            self.insert("1.0", text)
            self.see(tk.END)
            self.configure(state=tk.DISABLED)