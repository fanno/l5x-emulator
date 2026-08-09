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

        dummy:str = ""
        update = super().updateContent()
        if update and self.winfo_viewable():
            if status.Runing:
                total = "Total"
                text = f"------- {total:^30} -------  last (delayed) / max (S)\n"
                text += f"    {dummy:42} {status.Scan.Last:.4f} ({status.ScanDelayed:.4f}) / {status.Scan.Max:.4f}\n"
                text += f"Memory current/max (MB): {current:.2f} / {self._peak:.2f}\n"
                text += f"Count (number of plc scan): {status.Scan.Count}\n"

                for tname, task in status.Tasks.items():
                    text += f"\n------- {tname:^30} -------   last / max (S)\n"
                    text += f"    {dummy:42} {task.Last:.4f} / {task.Max:.4f}\n"
                    text += f"Count (number of plc scan): {task.Count}\n"

                    for pname, program in status.Programs[tname].items():
                        text += f"    {pname:42} {program.Last:.4f} / {program.Max:.4f}\n"

                opcua = "OPC UA"
                read = "Read"
                Write = "Write"
                text += f"\n------- {opcua:^30} -------   last / max (S)\n"
                text += f"    {read:42} {status.OpcUaRead.Last:.4f} / {status.OpcUaRead.Max:.4f}\n"
                text += f"    {Write:42} {status.OpcUaWrite.Last:.4f} / {status.OpcUaWrite.Max:.4f}\n"
                text += f"--------------------------------------------------------------"
            else:
                text = f"Initializing OPC UA server..."
            
            self.configure(state=tk.NORMAL)
            self.delete("1.0", tk.END)
            self.insert("1.0", text)
            self.see(tk.END)
            self.configure(state=tk.DISABLED)