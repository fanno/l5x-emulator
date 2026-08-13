import threading
import time
from typing import Dict, Union
from queue import Empty
from tkinter import Tk
from tkinter.scrolledtext import ScrolledText
from queue import Queue

from core.events import StatusEvent
T = Union[StatusEvent]
from core.emulator import Emulator

from eventbus.eventbus import EventListener, subscribe_event

from gui.tags.tags import TagsTabs
from gui.content import ContentTabs
from gui.emulatordialog import EmulatorDialog
from gui.menu import MenuFrame

class Gui():
    _root:Tk
    _status:ScrolledText
    _log:ScrolledText
    stopEvent: threading.Event
    _path:str
    _port:int
    _after_id: Dict[str, str]
    opc_thread:Emulator
    tagsTabs:TagsTabs = None
    threadStatus:StatusEvent = None
    queue:Queue[T]
    eventlistenet: EventListener
    _content:ContentTabs = None
    opc_thread = None
    forceOpcua = None

    def __init__(self, root:Tk, path:str, port:int, forceOpcua:bool):
        super().__init__()

        self._root = root
        self._path = path
        self._port = port
        self.forceOpcua = forceOpcua

        self.queue = Queue()
        self.eventlistenet = EventListener(self)
        self.stopEvent = threading.Event()

        self._after_id = {}

        self._root.geometry("880x800")
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.createMenu()
        self.updateTitle()

        #for development only
        try:
            self.create(self._path, self._port, self.forceOpcua)

            self._createUI()
        except Exception as e:
            from tkinter import messagebox
            import traceback
            messagebox.showerror("Error", traceback.format_exc())

    def createMenu(self):
        self.menu_bar = MenuFrame(self._root)
        
        self.menu_bar.add_menu("File", [
            ("Open...", self.open_emulator),
            ("Exit", self.on_closing)
        ])

    def open_emulator(self):
        dialog = EmulatorDialog(self._root, self._path, self._port, self.forceOpcua)
        self._root.wait_window(dialog)

        try:
            if dialog.file_path:
                path = dialog.file_path
                port = int(dialog.port_var.get())
                forceOpcua = bool(dialog.force_opcua_var.get())

                if path and port > 0:
                    port = int(dialog.port_var.get())

                    self._path = path
                    self._port = port
                    self.forceOpcua = forceOpcua

                    self.create(self._path, self._port, self.forceOpcua)

                    self._createUI()
        except Exception as e:
            from tkinter import messagebox
            import traceback
            messagebox.showerror("Error", traceback.format_exc())

    def on_closing(self):
        try:
            self.close()

            for key, task in self._after_id.items():
                self._root.after_cancel(task)

            self._root.destroy()
        finally:
            pass

    def create(self, path:str, port:int, forceOpcua:bool):
        self.close()
        
        self.opc_thread = Emulator(path, port, forceOpcua)
        self.opc_thread.start()

    def close(self):
        if self.opc_thread:
            self.opc_thread.stop()
            self.opc_thread.join()

            while self.opc_thread.is_alive():
                time.sleep(0.1)
            self.opc_thread = None

    def updateTitle(self, title=None):
        appName = "PLC Emulator"
        if title is None:
            title = "Application starting..."
        self._root.title(f"{appName}: {title}")

    def _createUI(self):
        if self._content is not None:
            self._content.destroy()

        self._content = ContentTabs(self._root)
        self._scedualQueue()

    def updateGUI(self):
        if self.threadStatus:
            self._content.updateContent(self.threadStatus)

            if self.threadStatus.Runing:
                self.updateTitle(f"{self.threadStatus.ControllerName} ({self.threadStatus.ControllerType}) {self.threadStatus.EndPoint}")
            else:
                self.updateTitle(f"Application starting on {self.threadStatus.EndPoint}")

    @subscribe_event(StatusEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def mainloop(self):
        self._root.mainloop()

    def _scedualQueue(self):
        if self._root.winfo_exists() and self.opc_thread:
            self._after_id["process_queue"] = self._root.after(200, self.process_queue)

    def process_queue(self):
        try:
            while self.opc_thread:
                event = self.queue.get_nowait()
                if isinstance(event, StatusEvent):
                    self.threadStatus = event
        except Empty:
            pass
        finally:
            self._scedualQueue()

        self.updateGUI()