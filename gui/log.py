import tkinter as tk

from gui.updatingscrolledtext import UpdatingScrolledText

from core.log import Logger

class LogText(UpdatingScrolledText):
    LEVEL_COLORS = {
        'DEBUG':    '#6c757d',
        'INFO':     '#28a745',
        'WARNING':  '#ffc107',
        'ERROR':    '#dc3545',
        'CRITICAL': '#ffffff',
    }

    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master,
            name=name,
            wrap=tk.WORD,
            state=tk.DISABLED)
        
        self._configure_tags()
        self.configure(state=tk.DISABLED)

    def _configure_tags(self):
        for level, fg in self.LEVEL_COLORS.items():
            bg = '#ffe6e6' if level == 'ERROR' else None
            if level == 'CRITICAL':
                bg = '#dc3545'
            self.tag_configure(level.upper(), foreground=fg, background=bg)
            self.tag_raise("sel")

    def updateContent(self, logger:Logger):
        update = super().updateContent()
        if update:        
            if logger.hasChanged():
                entries = logger.getLogs()
                self.configure(state=tk.NORMAL)
                self.delete("1.0", tk.END)
                for entry in entries:
                    self.insert(tk.END, f"\n\n{entry.message}" , entry.level.upper())
                self.see(tk.END)
                self.configure(state=tk.DISABLED)