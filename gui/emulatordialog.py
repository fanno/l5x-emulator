import tkinter as tk
from tkinter import messagebox, filedialog

class EmulatorDialog(tk.Toplevel):
    file_path:str = None

    def __init__(self, parent, path, port:int = 4840, forceOpcua:bool = False):
        super().__init__(parent)
        self.withdraw()

        self.title("Open L5X file")
        self.file_path = None
        
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        self.lift()
        self.focus_force()

        file_frame = tk.Frame(self)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(file_frame, text="File:").pack(side=tk.LEFT)
        
        self.file_var = tk.StringVar(value=path)
        tk.Entry(file_frame, textvariable=self.file_var, width=40).pack(side=tk.LEFT, padx=5)
        
        tk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.LEFT)
        
        port_frame = tk.Frame(self)
        port_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
        
        self.port_var = tk.StringVar(value=str(port))
        tk.Entry(port_frame, textvariable=self.port_var, width=10).pack(side=tk.LEFT, padx=5)

        self.force_opcua_var = tk.BooleanVar(value=forceOpcua)

        tk.Checkbutton(
            self,
            text="Force OPC UA",
            variable=self.force_opcua_var
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.positionDialog()
        self.deiconify()

    def positionDialog(self, offset_x=100, offset_y=100):
        self.parent.update_idletasks()

        x = self.parent.winfo_x() + offset_x
        y = self.parent.winfo_y() + offset_y
        
        self.geometry(f"+{x}+{y}")

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(
            parent=self,
            title="Select Emulator File",
            filetypes=[("Emulator Files", "*.L5X"), ("All Files", "*.*")]
        )
        if self.file_path:
            self.file_var.set(self.file_path)
    
    def ok(self):
        if not self.file_path:
            path = self.file_var.get()
            path = path.strip()
            if path:
                self.file_path = path

        if self.file_path:
            try:
                from lxml import etree
                parser = etree.XMLParser(strip_cdata=False)
                etree.parse(self.file_path, parser)
            except Exception:
                self.file_path = None

        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        try:
            port = int(self.port_var.get())
            if port < 1 or port > 65535:
                messagebox.showerror("Error", "Port must be 1-65535")
                return
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")

    def cancel(self):
        self.destroy()            