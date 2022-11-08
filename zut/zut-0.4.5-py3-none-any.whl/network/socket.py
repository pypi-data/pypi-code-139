from __future__ import annotations
import logging, socket
from contextlib import closing

logger = logging.getLogger(__name__)

def check_socket(host, port, timeout=1):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        try:
            returncode = sock.connect_ex((host, port))
            if returncode == 0:
                return True
            else:
                logger.debug("socket connnect_ex returned %d", returncode)
                return False
        except Exception as e:
            logger.debug("socket connnect_ex: %s", e)
            return False
