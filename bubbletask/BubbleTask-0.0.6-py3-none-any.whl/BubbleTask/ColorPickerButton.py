import tkinter as tk
from tkinter import ttk, colorchooser

from py_simple_ttk import (
    FocusedToplevel,
    hex_to_rgb,
    hex_to_rgba,
    rgba_to_hex,
    rgb_to_hex,
)

from .Spinbox import LabeledSpinbox

from typing import Callable


def extract_hex_alpha(h: str):
    """Converts hex to rgb tuple"""
    h = h[-2:]
    return [int(h[i : i + 2], 16) for i in range(1, 2, 2)]

def make_hex(color, alpha):
    return rgba_to_hex((*hex_to_rgb(color), int(alpha)))

def needs_white_text(color: str, barrier: int = 384) -> bool:
    """Returns True if luminance is under 50%"""
    if isinstance(color, str):
        if color.startswith("#"):
            if len(color) == 7:
                return sum(hex_to_rgb(color)) < barrier
            elif len(color) == 9:
                return sum(hex_to_rgba(color)[:3]) < barrier
    elif isinstance(color, list) or isinstance(color, tuple):
        if len(color) == 3:
            return sum(color) < barrier
        elif len(color) == 4:
            return sum(color) < barrier
    ValueError(f"Invalid color {color}")


class ColorPickerButton(ttk.Frame):
    def __init__(
        self,
        parent: ttk.Frame,
        text: str = "Select a color",
        command=None,
        default: str = None,
        **kwargs,
    ):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.label = ttk.Label(self, text=text, style="Bold.TLabel")
        self.label.pack(side=tk.LEFT)
        self.time, self.date = None, None
        self._command = command
        self.default = default
        self.var = tk.StringVar()
        self.var.set(self.default)
        self.button = tk.Button(self, textvariable=self.var, command=self.on_press)
        self.button.pack(side="left", fill="x")
        self.color_label = tk.Label(self, text=" ", bg=self.default, width=2)
        self.color_label.pack(side="left", fill="both")

    def on_press(self) -> None:
        col = colorchooser.askcolor(title="Select color")
        if col[1]:
            self.color_label.configure(bg=col[1])
            self.var.set(col[1])
            if self._command:
                self._command(self.get)

    def get(self) -> str:
        return self.var.get()

    def set(self, val: str) -> None:
        self.color_label.configure(bg=val)
        self.var.set(val)

    def clear(self) -> None:
        self.set(self.default)

class PickerWindow(FocusedToplevel):
    def __init__(
        self,
        window,
        on_select,
        title: str = "Select Color",
        start_color="#000000FF",
    ):
        if len(start_color) == 9:
            color = start_color[:-2]
            alpha = extract_hex_alpha(start_color)

        self.on_select = on_select

        def on_close(*args, **kwargs):
            self.destroy()

        FocusedToplevel.__init__(
            self,
            window=window,
            title=title,
            on_close=on_close,
        )

        self.color = ColorPickerButton(self.frame, default=start_color[:7])
        self.color.pack(side="top")

        r,g,b,a = hex_to_rgba(start_color)

        self.alpha = LabeledSpinbox(self.frame, "Alpha (0-255): ", from_=0, to=255, default=a)
        self.alpha.pack(side="top")

        ttk.Button(
            self.frame,
            command=self._on_select,
            text="Submit",
            style="LargeBold.TButton",
        ).pack(side="bottom", expand=True)

        self.resizable(False, False)
        self._finish_setup()

    def _on_select(self):
        print((self.color.get(), self.alpha.get()))
        self.on_select((self.color.get(), self.alpha.get()))
        self.destroy()


class ColorPickerButton2(ttk.Frame):
    def __init__(
        self, parent, text: str, default: str = None, command: Callable = None, **kwargs
    ):
        ttk.Frame.__init__(self, parent, **kwargs)

##        if len(default) == 7:
##            default += "FF"
##        print(default)
        
        self.label = ttk.Label(self, text=text, style="Bold.TLabel")
        self.label.pack(side=tk.LEFT)
        self.default, self._command = default, command
        self.var = tk.StringVar()
        self.var.set(self.default)
        self.color_label = tk.Label(
            self, textvariable=self.var, width=13
        )
        self.set(default)
        self.color_label.pack(side="right", fill="both")
        self.color_label.bind("<ButtonRelease-1>", self._on_click)

    def _on_click(self, event=None):
        def handle(val):
            col, opacity = val
            color = make_hex(col, opacity)
            self.set(color)
            self.color_label.configure(bg=color[:-2])
            if self._command:
                self._command(val)

        PickerWindow(self.winfo_toplevel(), handle, start_color=self.var.get())

    def get(self):
        return self.var.get()

    def set(self, val):
        self.var.set(val)
        bg = val[:-2]
        fg = "#FFFFFF" if needs_white_text(bg) else "#000000"
        self.color_label.configure(fg=fg,bg=bg)
