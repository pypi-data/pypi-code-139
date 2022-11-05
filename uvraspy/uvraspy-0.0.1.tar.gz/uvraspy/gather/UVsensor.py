import adafruit_ltr390
import board


class UVsensor:
    """
    Class used to gather information from the UVsensor

    The UV sensor needs to be connected to the Raspberry Pi in
    the following way:
    TODO list instruction to connect the sensor correctly.
    """

    def __init__(self):
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.ltr = adafruit_ltr390.LTR390(self.i2c)

    def readUV(self):
        return self.ltr.uvs

    def readUVI(self):
        return self.ltr.uvi

    def readAmbientLight(self):
        return self.ltr.light
