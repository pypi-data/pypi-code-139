import board
import adafruit_bmp280
import busio

# PT stands for Pressure and Temperature


class PTsensor:

    def __init__(self):
        # Initialize the sensor. Signal is connected to GPIO 8
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ptSensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    def readPressure(self):
        for i in range(3):
            try:
                pressure = self.ptSensor.pressure
                if pressure is not None:
                    return pressure
            except RuntimeError:
                continue
        raise Exception("Could not gather the pressure")
