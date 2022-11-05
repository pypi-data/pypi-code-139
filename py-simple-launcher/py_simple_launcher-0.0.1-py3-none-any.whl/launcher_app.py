import os, json
from py_simple_ttk import App, get_asset

defaults = {
    "application": "Launcher",
    "version": "0.0",
    "icon": get_asset("ico.png"),  # Set to icon path relative to script file
    "width": 400,
    "height": 400,
    "minwidth": 200,
    "minheight": 200,
    "scaling": 2,
    "scale_minsize": False,
    # "scale_startsize": True,
    "resizable_width": True,
    "resizable_height": True,
    "start_maximized": False,
    "enable_maximized": True,
    "start_fullscreen": False,
    "enable_fullscreen": True,
    "enable_themes_menu": True,
    "enable_launcher": True,
    # "movable_tabs": True,
    "enable_profiles": True,  # Enables a user profiles system.
    "conversations_enabled": False,
    "notes_enabled": False,
}


class LauncherApp(App):
    def __init__(self):
        if not os.path.exists("config.json"):
            with open("config.json", "w+") as f:
                json.dump(defaults, f, indent=4)
        App.__init__(self, "config.json")


if __name__ == "__main__":
    LauncherApp().mainloop()
