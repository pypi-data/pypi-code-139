import os, sys
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog

from py_simple_ttk import App

from .ProjectsTab import ProjectsTab
from .ViewerTab import ViewerTab
from .SettingsWindow import SettingsWindow

DEFAULT_USER_SETTINGS = {
    "background_image": None,
    "turn_red": True,
    "sunset_mode": False,
    "global_update_delay": 60,
    "default_update_delay": 50,
    "bubble_color": "#CCCCCCCC",
    "bubble_radius": 150,
    "bubble_text_size": 40,
    "bubble_overdue_color": "#FF647FCC",
    "text_color": "#FFFFFFFF",
    "task_bubble_color": "#CCCCEECC",
    "task_text_color": "#000000FF",
    "task_overdue_color": "#FF647FCC",
    "task_radius": 75,
    "task_text_size": 32,
    "line_thickness": 4,
    "line_blur": 3,
    "line_color": "#000000EE",
    "bubble_outline_color": "#CCCCCCCC",
    "task_outline_color": "#CCCCCCCC",
    "background_color": "#00000000",
    "task_outline_thickness": 3,
    "bubble_outline_thickness": 3,
}


class BubbleApp(App):
    def __init__(self):
        App.__init__(self, "config.json")
        self._on_profile_change()
        self.projects_tab = ProjectsTab(self)
        self.viewer_tab = ViewerTab(self)
        self.menu.add_command(label="Settings", command=self.show_settings)
        self.profiles.add_select_profile_action(self._on_profile_change)

    def _on_profile_change(self, *args):
        profile = self.profiles.current_profile
        update = False
        for k in DEFAULT_USER_SETTINGS:
            if not k in profile.data["preferences"]:
                profile.set_preference(k, DEFAULT_USER_SETTINGS[k])
                update = True
        if update:
            profile.save()

    def use_theme(self, *args, **kwargs):
        App.use_theme(self, *args, **kwargs)
        self.style.configure("LargeBold.TButton", font=self.large_bold_font)
        self.style.configure("HugeBold.TLabelframe.Label", font=self.large_bold_font)

    def show_settings(self):
        SettingsWindow(self)


if __name__ == "__main__":
    BubbleApp().mainloop()
