from queue import Empty

import psutil

import os

import threading

from tkinter import Tk
from tkinter.scrolledtext import ScrolledText

from typing import Dict, Union

from queue import Queue

from core.events import LogEvent, StatusEvent
T = Union[LogEvent, StatusEvent]
from eventbus.eventbus import EventListener, subscribe_event

from core.emulator import Emulator

from gui.log import Logger

from gui.tags.tags import TagsTabs

class Gui(EventListener):
    _root:Tk
    _status:ScrolledText
    _log:ScrolledText
    stopEvent: threading.Event
    _process:psutil.Process
    _peak:float
    _path:str
    _port:int
    _logger:Logger
    _after_id: Dict[str, str]
    running:bool
    opc_thread:Emulator
    tagsTabs:TagsTabs = None
    threadStatus:StatusEvent = None
    queue:Queue[T]

    def __init__(self, root:Tk, path:str, port:int):
        super().__init__()

        self.queue = Queue()

        self._logger = Logger()
        self._after_id = {}

        self._process:psutil.Process = psutil.Process(os.getpid())
        self._path = path
        self._port = port
        self._peak = 0.0
        self.after_id = {}
        self.running = True
        self.stopEvent = threading.Event()

        self._root = root
        self.updateTitle()

        self._root.geometry("880x800")
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.opc_thread = Emulator(self._path, self._port)
        self.opc_thread.start()

        self._createUI()
        self._scedualQueue()

    def on_closing(self):
        try:
            self.running = False
            if self.opc_thread:
                self.opc_thread.stop()
                self.opc_thread.join()

            for key, task in self._after_id.items():
                self._root.after_cancel(task)

            self._root.destroy()
        finally:
            pass

    def updateTitle(self, title=None):
        appName = "PLC Emulator"
        if title is None:
            title = "Application starting..."
        self._root.title(f"{appName}: {title}")

    def _createUI(self):
        self._status = ScrolledText(
            self._root,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            height=2
        )
        self._status.pack(fill="both", expand=False)

        self._status.pack(
            fill="x",
            expand=False
        )

        self._status.configure(state="normal")
        self._status.insert("1.0", "")
        self._status.configure(state="disabled")

        self._log = ScrolledText(
            self._root,
            wrap="word",
            state="disabled",
            font=("Consolas", 9),
            height=10
        )
        self._log.pack(fill="both", expand=False)

        self.tagsTabs = TagsTabs(self._root)

    def updateGUI(self, tags = {}):
        if self._status.focus_get() == self._status:
            return
        if self.threadStatus:

            if self.threadStatus.Data:
                self.tagsTabs.updateData(self.threadStatus.Data)

            current:float = self._process.memory_info().rss / 1024 / 1024
            if current > self._peak:
                self._peak = current

            if self.threadStatus.Runing:
                self.updateTitle(f"{self.threadStatus.ControllerName} ({self.threadStatus.ControllerType}) {self.threadStatus.EndPoint}")

                text = f"Scan time Current / max (Sec): {self.threadStatus.ScanCurrent:.3f} ({self.threadStatus.ScanDelayed:.3f}) / {self.threadStatus.ScanMax:.3f}, Scan count: {self.threadStatus.ScanCount}"
                text += f"\nMemory Current / max (MB): {current:.2f} / {self._peak:.2f}"
            else:
                self.updateTitle(f"Application starting on {self.threadStatus.EndPoint}")

                text = f"Initializing OPC UA server..."

            def _update():
                if self._status.focus_get() != self._status:
                    self._status.configure(state="normal")
                    self._status.delete("1.0", "end")
                    self._status.insert("1.0", text)
                    self._status.configure(state="disabled")

                if self._log.focus_get() != self._log:
                    if self._logger.hasChanged():
                        self._log.configure(state="normal")
                        self._log.delete("1.0", "end")
                        self._log.insert("end", "\n".join(self._logger.getLogs()) + "\n")
                        self._log.see("end")
                        self._log.configure(state="disabled")

            if self._root.winfo_exists() and self.running:
                self._after_id["_update"] = self._root.after(0, _update)

    @subscribe_event(LogEvent, StatusEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def mainloop(self):
        self._root.mainloop()

    def _scedualQueue(self):
        if self._root.winfo_exists() and self.running:
            self._after_id["process_queue"] = self._root.after(200, self.process_queue)

    def process_queue(self):
        try:
            while True:
                if self.opc_thread:
                    event = self.queue.get_nowait()
                    if isinstance(event, LogEvent):
                        self._logger.addEntry(event.message)
                    elif isinstance(event, StatusEvent):
                        self.threadStatus = event

        except Empty:
            pass
        finally:
            self._scedualQueue()

        self.updateGUI()