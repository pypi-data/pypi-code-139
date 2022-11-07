import os
import time
import pyautogui
from srutil import util
from typing import Literal, Optional


class Screenshot:
    def __init__(self, path: Optional[str] = None, name: Optional[str] = None,
                 img_format: Literal["png", "jpg", "jpeg"] = "png"):
        self.path = path if path is not None else os.getcwd()
        self.name = name
        self.format = util.stringbuilder(".", img_format)
        self.waiting_time = 5
        self.__can_take_now = False
        self.__current_time = None
        self.__shot = None
        self.__saved_in = None

    def __wait_for(self, in_secs: int):
        if in_secs is not None:
            self.waiting_time = in_secs
        self.__can_take_now = True
        time.sleep(self.waiting_time)
        return self

    def take(self, in_secs: int = 5) -> "Screenshot":
        if self.__can_take_now is False:
            self.__wait_for(in_secs)
            self.__current_time = util.now()
            if self.name is None:
                self.name = util.stringbuilder("Screenshot_", self.__current_time.strftime("%d%m%Y_%H%M%S"),
                                               self.format)
        if self.__can_take_now is False:
            self.take(in_secs)
        self.__shot = pyautogui.screenshot()
        self.__can_take_now = False
        return self

    def display(self):
        if self.__shot is None:
            raise Exception("Screenshot should be taken before Displaying")
        self.__shot.show()

    def save(self) -> bool:
        if self.__shot is None:
            raise Exception("Screenshot should be taken before Saving")
        if os.path.splitext(self.name)[-1].lower() not in [".png", ".jpg", ".jpeg"]:
            self.name += self.format
        self.__saved_in = os.path.abspath(util.stringbuilder(self.path, self.name, separator="/"))
        self.name = None
        self.__shot.save(self.__saved_in)
        return os.path.exists(self.__saved_in)

    def get_screenshot_path(self) -> str:
        return self.__saved_in
