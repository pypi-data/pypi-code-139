import tkinter as tk
from tkinter import ttk

from py_simple_ttk import (
    App,
    FocusedToplevel,
    Tab,
    LabeledMultiCheckbutton,
    LabeledPathEntry,
    LabeledFloatEntry,
)


class ApplicationSettings(Tab):
    def __init__(self, notebook):
        Tab.__init__(self, notebook, "Application")
        (frame := ttk.Frame(self)).pack(fill="both", expand=True, padx=25, pady=20)


class RendererSettings(Tab):
    def __init__(self, notebook):
        Tab.__init__(self, notebook, "Renderer")
        (frame := ttk.Frame(self)).pack(fill="both", expand=True, padx=25, pady=20)
        conf = {
            "turn_red": (
                [],
                {
                    "text": "Turn bubble red after deadline",
                    # "default": False,
                    "replace_output": [False, True],
                },
            ),
            "sunset_mode": (
                [],
                {
                    "text": "Bubble continues sinking after deadline",
                    # "default": False,
                    "replace_output": [False, True],
                },
            ),
        }

        self.widgets = LabeledMultiCheckbutton(frame, "Renderer Settings", conf)
        self.widgets.pack(side="top", fill="x")
        self.widgets.add(
            self.widgets,
            "background_image",
            (),
            {"is_child": True, "default": ""},
            widget_type=LabeledPathEntry,
        )
        self.widgets.add(
            self.widgets,
            "global_update_delay",
            (),
            {"is_child": True},
            widget_type=LabeledFloatEntry,
        )


class SettingsWindow(FocusedToplevel):
    def __init__(self, app: App):
        FocusedToplevel.__init__(self, window=app.window)
        self._finish_setup()
        self.app = app
        self.profile = app.profiles.current_profile
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)
        self.renderer_settings = RendererSettings(self.notebook)
        ttk.Button(self.frame, text="Save", command=self.save).pack(
            side="top", fill="x"
        )
        self.tabs = [self.renderer_settings]
        self.load()

    def save(self) -> bool:
        for t in self.tabs:
            for k in (settings := t.widgets.get()):
                self.profile.set_preference(k, settings[k])
        return self.profile.save()

    def load(self) -> None:
        for t in self.tabs:
            for k in list(t.widgets.widgets.keys()):
                t.widgets.widgets[k].set(self.profile.get_preference(k))
