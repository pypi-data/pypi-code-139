from sys import stdout
import subprocess

class PingerTools:
    def __init__(self):
        pass
    
    def ping_address(self, target_addr=None):
        if target_addr:
            pingproc = subprocess.Popen(["ping", "-c", "3", target_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = pingproc.communicate()
            stdout.write(output.decode('utf-8'))

if __name__ == "__main__":
    pt = PingerTools()
    pt.ping_address("google.com")