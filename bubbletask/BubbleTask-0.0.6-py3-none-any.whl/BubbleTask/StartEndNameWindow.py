from tkinter import ttk

from py_simple_ttk import FocusedToplevel, LabeledEntry, NoticeWindow

from .TimeSelectionButton import TimeSelectionButton
from .BubbleLib import parsetimes


class StartEndNameWindow(FocusedToplevel):
    def __init__(
        self,
        window,
        on_complete,
        title="Set a name and times...",
        start_text="Set Start ",
        end_text="Set End ",
        entry_text="Name ",
        default_start: float = None,
        default_end: float = None,
        name: str = None,
    ):
        FocusedToplevel.__init__(self, window=window)
        self.title(title)
        self.start_entry = TimeSelectionButton(
            self.frame, text=start_text, default=default_start
        )
        self.start_entry.pack(expand=False, fill="x", side="top", padx=20, pady=(25, 5))
        self.end_entry = TimeSelectionButton(
            self.frame, text=end_text, default=default_end
        )
        self.end_entry.pack(expand=False, fill="x", side="top", padx=20, pady=5)

        def submit(*args, **kwargs):
            try:
                on_complete(
                    self.name_entry.get(),
                    parsetimes(*self.start_entry.get()),
                    parsetimes(*self.end_entry.get()),
                )
            except Exception as e:
                NoticeWindow(window=self, text=f"Error - {e}")

        self.name_entry = LabeledEntry(self.frame, labeltext=entry_text, command=submit)
        self.name_entry.pack(expand=False, fill="x", side="top", padx=20, pady=5)
        if not name is None:
            self.name_entry.set(name)
        b = ttk.Button(self.frame, text="Submit", command=submit)
        b.pack(fill="x", side="top", padx=20, pady=(5, 25))
        self._finish_setup()


class NewProjectWindow(StartEndNameWindow):
    def __init__(self, window, on_complete, **kwargs):
        StartEndNameWindow.__init__(
            self,
            window,
            on_complete,
            title="New Project",
            entry_text="Project Name ",
            **kwargs,
        )


class NewTaskWindow(StartEndNameWindow):
    def __init__(self, window, on_complete, **kwargs):
        StartEndNameWindow.__init__(
            self,
            window,
            on_complete,
            title="New Task",
            entry_text="Task Name ",
            **kwargs,
        )


class EditTaskWindow(StartEndNameWindow):
    def __init__(self, window, on_complete, task, **kwargs):
        StartEndNameWindow.__init__(
            self,
            window,
            on_complete,
            title=f"Edit Task: {task.name}",
            entry_text="Task Name ",
            default_start=task.start,
            default_end=task.deadline,
            name=task.name,
            **kwargs,
        )
