from importlib import import_module


class ChamberHandler(object):
    def __init__(self, driver, connection, port=None, timeout=30, time_sleep=5):
        """
        :param driver - is the power control driver module name to be imported:
        :param connection - is the power control ssh or telnet connection created in the station config:
        :param port - port: (str)
        :param timeout - timeout: (int)
        :param time_sleep - time_sleep: (int)
        :return None
        Example:
            p = lib.ChamberInterface(driver='watlow', connection=lib.getconnections()['WATLOW'], timeout=10)
            p.on()
            p.off()
            or
            p = lib.ChamberInterface(driver='watlow', connection=lib.getconnections()['WATLOW'])
            p.on(port='A1 A2')
            p.off(port='A1 A2')
        """
        self._connection = connection
        self._port = port
        self._timeout = timeout
        self.time_sleep = time_sleep
        module = import_module(f"{__name__.rsplit('.', 1)[0]}.driver.{driver}")
        self.cont = module.Controller(connection=self._connection)

    def identify(self):
        self.cont.identify()

    def chamber_profile(self, temperature, ramp_rate, margin=0.2, soak=None):
        self.identify()
        self.ramp_rate(rate=ramp_rate)
        self.ramp(temperature=temperature)
        self.monitor(temperature=temperature, delay=ramp_rate, margin=margin)
        self.soak(delay=soak) if soak else None

    def ramp_conf(self, temperature, rate, duration):
        self.cont.ramp_conf(temperature, rate, duration)

    def ramp(self, temperature):
        pass

    def monitor(self, temperature, delay, margin, timeout=None):
        temperature = float(temperature)
        margin = float(margin)
        with lib.TimeIt() as t:
            while True:
                temp = self.cont.read_temp()
                log.debug(f'Chamber Temp: [ {temp} C ]')
                save_file(f'{temp} C', 'Chamber_Temp.log')

                if temperature - margin <= temp <= temperature + margin:
                    return True
                if timeout and t.duration >= int(timeout):
                    lib.fail()
                time.sleep(int(delay))

    @staticmethod
    def soak(delay):
        self.cont.identify(delay)
