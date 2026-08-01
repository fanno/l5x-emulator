import tkinter as tk
from typing import List, Tuple, Callable

class MenuFrame(tk.Frame):
    
    def __init__(self, parent: tk.Widget, bg: str = "#f3f3f3"):
        super().__init__(parent, bg=bg, height=30)
        self.pack_propagate(True)  # Respect height
        
        self.bg = bg
        self.hover_bg = "#bababa"
        self.fg = "#000000"
        
        self.buttons: dict[str, tk.Button] = {}
        self.popups: dict[str, tk.Menu] = {}

        self.pack(fill=tk.X, expand=tk.FALSE)
        
    def add_menu(self, label: str, commands: List[Tuple[str, Callable]]) -> None:

        btn = tk.Button(
            self,
            text=label,
            bg=self.bg,
            fg=self.fg,
            relief=tk.FLAT,
            padx=10,
            pady=0,
            font=("Arial", 10),
            command=lambda: self._show_popup(label)
        )
        btn.pack(side=tk.LEFT)
        self.buttons[label] = btn
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.hover_bg))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.bg))
        
        popup = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg)
        for cmd_label, cmd_func in commands:
            popup.add_command(label=cmd_label, command=cmd_func)
        self.popups[label] = popup
    
    def _show_popup(self, label: str) -> None:
        btn = self.buttons[label]
        popup = self.popups[label]
        
        x = self.master.winfo_rootx() + btn.winfo_x()
        y = self.master.winfo_rooty() + self.winfo_height()
        popup.tk_popup(x, y)
    
    def enable_keyboard_shortcuts(self, shortcuts: dict[str, str]) -> None:
        for key, menu_label in shortcuts.items():
            self.master.bind(f"<Alt-{key.lower()}>", 
                           lambda e, l=menu_label: self._show_popup(l))