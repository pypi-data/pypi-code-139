import time
import parse
import logging

_log = logging.getLogger(__name__)


class Controller(object):
    def __init__(self):
        self._connection = connection
        self._prompt = '\n'

    def identify(self):
        model = '29949|29951'
        self.cb.send('*IDN?\n', expectphrase='\n', check_received_string='29949|29951')
        self.write_and_read('*IDN?')
        if not self.check_received_string(model):
            lib.fail(f'Chamber Wrong Model - {model}')

    def start(self):
        pass

    def stop(self):
        pass

    def read_temp(self):
        data = self.write_and_read(':SOURCE:CLOOP1:PVALUE?\n')
        time.sleep(1)
        if temp := re.search(r'\s(\d+\.\d+|\d+)', data):
            return float(temp.group(1))
        lib.fail(f'Chamber Temperature reading Fail - {data}')

    def read_humi(self):
        data = self.write_and_read(':SOURCE:CLOOP1:PVALUE?\n')
        if temp := re.search(r'\s(\d+\.\d+|\d+)', data):
            return float(temp.group(1))
        lib.fail(f'Chamber humidity reading Fail - {data}')

    def soak_conf(self, temperature):
        return

    def ramp_conf(self, temperature, rate, duration=None, **kwargs):
        self.write_and_read(f':SOURCE:CLOOP1:SPOINT {temperature}\n')
        data = self.write_and_read(f':SOURCE:CLOOP1:SPOINT?\n')
        if temperature not in data:
            lib.fail(f"Chamber ramp temperature config '{temperature}' fail")
        self.write_and_read(f':SOURCE:CLOOP1:RTIME {rate}\n')
        data = self.write_and_read(f':SOURCE:CLOOP1:RTIME?\n')
        if temperature not in data:
            lib.fail(f"Chamber ramp rate config '{data}' fail")

    def write_and_read(self, cmd):
        self._connection.send(f'{cmd}\n', expectphrase=self._prompt, timeout=10)
        time.sleep(1)
        return self._connection.recbuf
