import curses
import threading

from betterTUI.Screen import Screen

class Text:
    def __init__(self, screen: Screen, x: int, y: int, content: str, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.content = content
        self.parent = None
        self.timer = None
        self.deleted = False

        screen.addstr(y, x, content, *args)

    # Beta Feature
    def real_time_update(self, interval: int, func):
    
        def update():
            if not(self.deleted):
                self.timer = threading.Timer(interval, update).start()
                y, x = self.screen.getyx()
                self.screen.addstr(self.y, self.x, func())
                self.screen.move(y, x)
                self.screen.refresh()

        update()

    def delete(self):
        self.screen.addstr(self.y, self.x, " " * len(self.content))
        self.deleted = True

        del self