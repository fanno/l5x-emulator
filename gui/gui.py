from queue import Empty

import threading

from tkinter import Tk

from tkinter.scrolledtext import ScrolledText

from typing import Dict, Union

from queue import Queue

from core.events import LogEvent, StatusEvent
T = Union[LogEvent, StatusEvent]
from eventbus.eventbus import EventListener, subscribe_event

from core.emulator import Emulator

from core.log import Logger

from gui.tags.tags import TagsTabs
from gui.content import ContentTabs

class Gui(EventListener):
    _root:Tk
    _status:ScrolledText
    _log:ScrolledText
    stopEvent: threading.Event
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

        self._path = path
        self._port = port
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
        self._content = ContentTabs(self._root)

    def updateGUI(self, tags = {}):
        if self.threadStatus:
            self._content.updateContent(self.threadStatus, self._logger)

            if self.threadStatus.Runing:
                self.updateTitle(f"{self.threadStatus.ControllerName} ({self.threadStatus.ControllerType}) {self.threadStatus.EndPoint}")
            else:
                self.updateTitle(f"Application starting on {self.threadStatus.EndPoint}")

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
                        self._logger.addEntry(event)
                    elif isinstance(event, StatusEvent):
                        self.threadStatus = event

        except Empty:
            pass
        finally:
            self._scedualQueue()

        self.updateGUI()