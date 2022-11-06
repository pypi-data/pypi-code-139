import tkinter as tk
from tkinter import ttk

import time, datetime

from py_simple_ttk import LabeledButtonEntry, LabeledEntry, MultiWidgetMixin, Labeler

from .DatePicker import DatePicker
from .BubbleLib import parsetimes


class TimeSelectionButton(ttk.Frame):
    def __init__(
        self,
        parent: ttk.Frame,
        text: str = "Select a time",
        command=None,
        default: float = None,
        **kwargs,
    ):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.time, self.date = None, None
        self._command = command

        self.entry = LabeledButtonEntry(
            self,
            text,
            # button_text=self._get_timestring(),
            command=self.on_press,
        )
        self.entry.configure(width=0)
        self.set_by_timestamp(default)
        self.default_time, self.default_date = self.time, self.date
        self.entry.pack(side="top", fill="x")
        self.entry.button.configure(text=self._get_timestring())
        self.entry.button.pack(fill="x", expand=True)
        self.toplevel = None

    def _get_timestring(self):
        ts = f"{self.date} @ " if self.date else "... @ "
        t = self.time
        ts += f"{t[0]}:{t[1]} {t[2]}" if t else "..."
        return ts

    def on_press(self, _=None):
        if not self.toplevel:

            def handle_selection(value):
                print(type(value[0]))
                print("Date", value[0])
                print("Time", value[1])
                self._set_date(value[0])
                self._set_time(value[1])
                self.update_button_text()
                self.toplevel.destroy()
                self.toplevel = None
                if self._command:
                    self._command(self.get())

            def cancel():
                self.toplevel.destroy()
                self.toplevel = None

            self.toplevel = DatePicker(
                self.winfo_toplevel(),
                handle_selection,
                cancel,
                start_time=self.time,
                start_date=self.date,
            )

    def set_label(self, date, start_time):
        self._set_date(date)
        self._set_time(start_time)
        self.update_button_text()

    def get(self) -> tuple:
        return self.date, self.time

    def _set_date(self, date):
        self.date = date

    def set_date(self, date):
        self._set_date(date)
        self.update_button_text()

    def _set_time(self, t):
        self.time = t

    def set_time(self, t):
        self._set_time(t)
        self.update_button_text()

    def clear(self):
        self.date, self.time = None, None
        self.set_time(self.default_time)
        self.set_date(self.default_date)
        self.update_button_text()

    def update_button_text(self):
        self.entry.button.configure(text=self._get_timestring())

    def set_by_timestamp(self, timestamp: float):
        if timestamp:
            dt = datetime.datetime.fromtimestamp(timestamp)
            self.set_time(dt.strftime("%H %M %p").split(" "))
            self.set_date(dt.strftime("%m/%d/%y"))


class LabeledTimeSelectionButton(Labeler, TimeSelectionButton):
    """Labeled TimeSelectionButton with the Super Widget mixin"""

    __desc__ = """Set custom_values keyword to "False" to disable custom user-entered values. Set the "default" keyword to the index of the value to display by default from the "values" keyword."""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        command=None,
        custom_values: bool = True,
        labelside: str = tk.LEFT,
        is_child: bool = False,
        **kw,
    ):
        # self.default = values[default] if any(values) else ""
        Labeler.__init__(
            self, parent, labeltext, labelside=labelside, header=not is_child
        )
        TimeSelectionButton.__init__(self, self.frame, command=command, **kw)
        TimeSelectionButton.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        self.is_child = is_child

    # def disable(self):
    #     """Disable Combobox. `Returns None`"""
    #     self["state"] = tk.DISABLED

    # def enable(self):
    #     """Enable Combobox. `Returns None`"""
    #     self["state"] = self._state


class LabeledMultiTimeSelectionButton(Labeler, ttk.Frame, MultiWidgetMixin):
    """Labeled MultiWidget LabeledTimeSelectionButton"""

    def __init__(
        self,
        parent: ttk.Frame,
        labeltext: str,
        config: dict,
        is_child: bool = False,
        labelside=tk.TOP,
    ):
        Labeler.__init__(
            self, parent, labeltext, labelside=labelside, header=not is_child
        )
        ttk.Frame.__init__(self, self.frame)
        ttk.Frame.pack(self, fill=tk.BOTH, expand=True, side=tk.TOP)
        MultiWidgetMixin.__init__(self, LabeledTimeSelectionButton, config)
        self.is_child = is_child
