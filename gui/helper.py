from tkinter import ttk

def getParentTab(content):
    widget = content.master
    while widget is not None:
        if isinstance(widget, ttk.Notebook):
            for tab_id in widget.tabs():
                tab_widget = widget.nametowidget(tab_id)
                w = content
                while w is not None:
                    if w is tab_widget:
                        return (widget, tab_id)
                    w = w.master
        widget = widget.master

    return (None, None)