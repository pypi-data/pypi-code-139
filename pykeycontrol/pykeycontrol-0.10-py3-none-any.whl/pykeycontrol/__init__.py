import os
import keyboard


class StopStart:
    def __init__(
            self,
            hotkey_enable="ctrl+alt+p",
            hotkey_disable="ctrl+alt+o",
            hotkey_hc_exit="ctrl+alt+e",
    ):
        self.stop = True
        self.hotkey_enable = hotkey_enable
        self.hotkey_disable = hotkey_disable
        self.hotkey_hc_exit = hotkey_hc_exit

    def hc_exit(self):
        print("HARDCORE EXIT! FTW!")
        os._exit(1)

    def disable(self):
        self.stop = True
        print("Disabled!")
        return self

    def enable(self):
        self.stop = False
        print("Enabled!")
        return self

    def reset_all_hotkeys(self):
        try:
            keyboard.clear_all_hotkeys()
        except Exception:
            pass
        return self

    def add_hotkeys(self):
        keyboard.add_hotkey(self.hotkey_enable, self.enable)
        keyboard.add_hotkey(self.hotkey_disable, self.disable)
        keyboard.add_hotkey(self.hotkey_hc_exit, self.hc_exit)

        return self

