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
        if update:
            if status.Runing:
                text = f"Scan time current (Sec): {status.ScanCurrent:.3f} ({status.ScanDelayed:.3f})"
                text += f"\nScan time longest (Sec): {status.ScanMax:.3f}"
                text += f"\nScan count (number of plc scan): {status.ScanCount}"
                text += f"\n\nMemory current (MB): {current:.2f}"
                text += f"\nMemory max (MB): {self._peak:.2f}"
            else:
                text = f"Initializing OPC UA server..."
            
            self.configure(state=tk.NORMAL)
            self.delete("1.0", tk.END)
            self.insert("1.0", text)
            self.see(tk.END)
            self.configure(state=tk.DISABLED)