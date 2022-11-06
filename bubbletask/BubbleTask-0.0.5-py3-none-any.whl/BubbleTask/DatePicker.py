import datetime

import tkinter as tk
from tkinter import ttk

from py_simple_ttk import (
    FocusedToplevel
)

from tkcalendar import Calendar
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants as tpConstants

class DatePicker(FocusedToplevel):
    def __init__(
        self,
        window,
        on_select,
        on_close,
        title: str = "Select Date",
        start_time: float = None,
        start_date: datetime.datetime=None,
    ):
        self.on_select = on_select
        FocusedToplevel.__init__(
            self,
            window=window,
            title=title,
            on_close=on_close,
        )
        (frame := ttk.Frame(self)).pack(fill="both", expand=True)
        self.clock = SpinTimePickerModern(frame)
        self.clock.pack(side="top", expand=False, fill=tk.BOTH)
        self.clock.addAll(tpConstants.HOURS24)
        self.clock.configureAll(
            bg="#404040",
            height=1,
            fg="#ffffff",
            font=("Times", 16),
            hoverbg="#404040",
            hovercolor="#d73333",
            clickedbg="#2e2d2d",
            clickedcolor="#d73333",
        )
        self.clock.configure_separator(bg="#404040", fg="#ffffff")
        self.calendar = Calendar(frame, selectmode="day")
        self.calendar.pack(side="top", fill=tk.BOTH)
        ttk.Button(
            frame,
            command=self._on_select,
            text="Select Time and Data",
            style="LargeBold.TButton",
        ).pack(side="top", expand=True)

        self.resizable(False, False)
        self._finish_setup()

    def _on_select(self) -> bool:
        return self.on_select((self.calendar.get_date(), self.clock.time()))
