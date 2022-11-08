from .ZoneSenderObject import ZoneSenderObject


class CanDiagMessage(ZoneSenderObject):
    def __init__(self, id: int, cmd: list):
        super().__init__()
        self.id = id
        self.cmd = cmd