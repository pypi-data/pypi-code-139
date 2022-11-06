import tkinter as tk
from tkinter import ttk

from py_simple_ttk import (
    Labeler, MultiWidgetMixin, SuperWidgetMixin
)
from typing import Callable

class LabeledSpinbox(Labeler, ttk.Spinbox, SuperWidgetMixin):
    """Labeled Spinbox with the Super Widget mixin"""
    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        command: Callable = None,
        default: int = 0,
        on_keystroke: bool = False,
        bind_enter: bool = True,
        bind_escape_clear: bool = True,
        bind_mouse_wheel: bool = True,
        custom_values: bool = True,
        labelside: str = tk.LEFT,
        is_child: bool = False,
        fill:str = "x",
        expand:bool = False,
        width=8,
        widgetargs={},
        **kw
    ):
        self.var = tk.StringVar()
        self.default = default
        self.var.set(self.default)
        Labeler.__init__(
            self, parent, labeltext, labelside=labelside, header=not is_child
        )
        ttk.Spinbox.__init__(self, self.frame, textvariable=self.var, width=width,**kw)
        ttk.Spinbox.pack(self, expand=expand, side="right")
        SuperWidgetMixin.__init__(self, **widgetargs)

        self.is_child = is_child

        self._state = "normal" if custom_values else "readonly"
        self._command = command
        if on_keystroke:
            self.bind("<KeyRelease>", self._on_execute_command)
        if bind_enter:
            self.bind("<Return>", self._on_execute_command)
        if bind_escape_clear:
            self.bind("<Escape>", self.clear())
        if bind_mouse_wheel:
            self.bind("<MouseWheel>", self._on_execute_command)

    def disable(self):
        """Disable Spinbox. `Returns None`"""
        self["state"] = tk.DISABLED

    def enable(self):
        """Enable Spinbox. `Returns None`"""
        self["state"] = self._state

    def get(self):
        """Get Spinbox value. `Returns a String`"""
        return self.var.get()

    def set(self, val: str):
        """Set Spinbox value. `Returns None`"""
        self.var.set(val)

    def clear(self):
        """Sets Spinbox to its default value. `Returns None`"""
        self.var.set(self.default)

    def _on_execute_command(self, event=None):
        """Calls the provided "command" function with the contents of the Entry. `Returns None`"""
        if self._command:
            self._command(self.get())


if __name__ == "__main__":
    root = tk.Tk()
    spin = LabeledSpinbox(root, from_=0, to=255, state="readonly")
    spin.pack()
    root.mainloop()
