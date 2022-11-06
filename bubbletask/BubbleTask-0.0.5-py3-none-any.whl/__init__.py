from .BubbleTask import BubbleApp
import os, json

if not os.path.isfile("config.json"):
    with open("config.json", "w+") as f:
        json.dump(
            {
                "application": "BubbleTask",
                "version": "0.0.3",
                "width": 700,
                "height": 600,
                "minwidth": 700,
                "minheight": 600,
                "resizable_width": True,
                "resizable_height": True,
                "start_maximized": False,
                "start_fullscreen": False,
                "enable_fullscreen": True,
                "scaling": 1.2,
                "enable_themes_menu": True,
                "enable_users": True,
                "movable_tabs": False,
                "conversations_enabled": False,
                "notes_enabled": False,
            },
            f,
        )
