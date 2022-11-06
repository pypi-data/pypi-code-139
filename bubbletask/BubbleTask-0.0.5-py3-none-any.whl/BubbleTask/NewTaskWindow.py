from tkinter import ttk

from py_simple_ttk import FocusedToplevel, LabeledEntry

from .TimeSelectionButton import TimeSelectionButton
from .BubbleLib import parsetimes


class NewTaskWindow(FocusedToplevel):
    def __init__(self, window, on_complete):
        FocusedToplevel.__init__(self, window=window)
        self.on_complete = on_complete

        self.start_time_entry = TimeSelectionButton(self.frame, text="Set Start ")
        self.start_time_entry.pack(
            expand=False, fill="x", side="top", padx=20, pady=(25, 5)
        )

        self.end_time_entry = TimeSelectionButton(self.frame, text="Set End ")
        self.end_time_entry.pack(expand=False, fill="x", side="top", padx=20, pady=5)

        self.entry = LabeledEntry(
            self.frame,
            labeltext="Task Name ",
            bind_enter=True,
            command=self._on_submit,
        )
        self.entry.pack(expand=True, fill="x", side="top", padx=20, pady=5)
        ttk.Button(
            self.frame,
            text="Submit",
            command=self._on_submit,
        ).pack(fill="x", side="top", padx=20, pady=(5, 25))
        self._finish_setup()

    def _on_submit(self, *args, **kwargs):
        self.on_complete(
            self.entry.get(),
            parsetimes(*self.start_time_entry.get()),
            parsetimes(*self.end_time_entry.get()),
        )
