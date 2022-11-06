class UVCalculator:
    """
    Class to calculate if there is too much UV
    .
    Attributes
    ----------
    bluetooth : BluetoothHandler
        bluetooth handler that is used to communicate with other devices
    """
    inst = None
    MIN_UV = 2
    UV_DECREASE = 1 / 120 / 5
    UPDATE_TIME = 5
    RESET_THRESHOLD = 24

    def uv(skintype, uv_index):
        pass

    def __init__(self, main):
        self.value = 0
        self.main = main
        self.progress = 0
        self.last_time = 0
        UVCalculator.inst = self

    def updateUV(self, value, time):
        # self.main.warn(str(t) + " UV value updated: " + str(value))

        if self.last_time < time - self.UPDATE_TIME * self.RESET_THRESHOLD:
            # reset counter
            self.progress = 0

        if value < self.MIN_UV:
            self.progress -= self.UV_DECREASE * self.UPDATE_TIME
            return

    def supress(self):
        pass
