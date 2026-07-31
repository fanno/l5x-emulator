from typing import Dict, Union
from collections import deque

from queue import Queue, Empty

from tkinter.ttk import Notebook, Frame
import tkinter as tk

from gui.fault.faultgrid import FaultGrid
from gui.fault.log import LogText

from core.events import  MinorFaultEvent, MajorFaultEvent

from engine.errors import MinorFault, MajorFault

T = Union[MinorFaultEvent, MajorFaultEvent]
from eventbus.eventbus import EventListener, subscribe_event

class FaultTabs(Notebook):
    tabs:dict[str, FaultGrid]
    _after_id: Dict[str, str]
    eventListener:EventListener

    Minorfaults:list[MinorFault]
    Majorfault:list[MajorFault]

    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.name = name

        self.minorCounter = 0
        self.majorCounter = 0

        self.queue = Queue()
        self.Majorfault = deque(maxlen=100)
        self.Minorfaults = deque(maxlen=100)

        self.eventListener = EventListener(self)

        titel = "Major fault"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.major = FaultGrid(frame,
                               name=titel,
                               show='tree headings',
                               selectmode=tk.NONE)

        titel = "Minor fault"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.minor = FaultGrid(frame,
                               name=titel,
                               show='tree headings',
                               selectmode=tk.NONE)

        titel = "Excaption Log"
        frame = Frame(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.add(frame, text=titel)
        self.log = LogText(frame, name=titel)

        self.pack(fill=tk.BOTH, expand=True)

        self._after_id = {}
        self._UpdateUI()

    @subscribe_event(MinorFaultEvent, MajorFaultEvent)
    def on_eventbus(self, event):
        self.queue.put_nowait(event)

    def process_queue(self):
        try:
            while True:
                event = self.queue.get_nowait()
                if isinstance(event, MinorFaultEvent):
                    self.minorCounter += 1
                    self.Minorfaults.appendleft(event.fault)
                elif isinstance(event, MajorFaultEvent):
                    self.majorCounter += 1
                    self.Majorfault.appendleft(event.fault)
        except Empty:
            pass
        finally:
            pass

    def process_faults(self):
        self.process_queue()
        self.minor.updateContent(self.Minorfaults, self.minorCounter)
        self.major.updateContent(self.Majorfault, self.majorCounter)

        self._UpdateUI()

    def _UpdateUI(self):
        if self.winfo_exists():
            self._after_id["process_queue"] = self.after(1000, self.process_faults)