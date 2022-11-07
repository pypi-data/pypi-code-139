import shlex
from subprocess import Popen, PIPE
import codecs


# return stdout, stderr
# raise exception if failed to execute
def run(cmd, timeout=None):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    stdout_b, stderr_b = proc.communicate(timeout=timeout)
    return codecs.decode(stdout_b).strip(), codecs.decode(stderr_b).strip()
