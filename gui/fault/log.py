from typing import Union, Dict
from queue import Queue, Empty

import tkinter as tk

from core.events import LogEvent
T = Union[LogEvent]
from eventbus.eventbus import EventListener, subscribe_event

from gui.updatingscrolledtext import UpdatingScrolledText

from core.log import Logger

class LogText(UpdatingScrolledText):
    LEVEL_COLORS = {
        'DEBUG':    "#111313",
        'INFO':     "#1332e6",
        'WARNING':  "#FFC400",
        'ERROR':    '#dc3545',
        'CRITICAL': '#ffffff',
    }

    _after_id: Dict[str, str]
    queue:Queue[T]    
    logger:Logger
    eventlistenet: EventListener

    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master,
            name=name,
            wrap=tk.WORD,
            state=tk.DISABLED)

        self._after_id = {}

        self.eventlistenet = EventListener(self)

        self.queue = Queue()
        self.logger = Logger()
        
        self._configure_tags()
        self.configure(state=tk.DISABLED)

        self._scedualQueue()

    def _configure_tags(self):
        for level, fg in self.LEVEL_COLORS.items():
            bg = '#ffe6e6' if level == 'ERROR' else None
            if level == 'CRITICAL':
                bg = self.LEVEL_COLORS['ERROR']
            elif level == 'WARNING':
                bg = "#464444"
            self.tag_configure(level.upper(), foreground=fg, background=bg)
            self.tag_raise("sel")

    def updateContent(self):
        update = super().updateContent()
        if update and self.winfo_viewable():
            if self.logger.hasChanged():
                entries = self.logger.getLogs()
                self.configure(state=tk.NORMAL)
                self.delete("1.0", tk.END)
                for entry in entries:
                    self.insert(tk.END, f"\n\n{entry.message}" , entry.level.upper())
                self.see(tk.END)
                self.configure(state=tk.DISABLED)

    @subscribe_event(LogEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def process_queue(self):
        try:
            while True:
                event = self.queue.get_nowait()
                if isinstance(event, LogEvent):
                    self.logger.addEntry(event)
        except Empty:
            pass
        finally:
            self._scedualQueue()
        self.updateContent()

    def _scedualQueue(self):
        if self.winfo_exists():
            self._after_id["process_queue"] = self.after(1000, self.process_queue)