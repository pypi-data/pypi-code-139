from skyway.service import *
from importlib import import_module
from time import time, sleep
import sys, os, signal
    
service_name = sys.argv[1]
status = 'testing' if '--test' in sys.argv else 'running'

import logging
logging.basicConfig(filename=cfg['paths']['log'] + service_name + '.log', format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logging.info('Service daemon started.')

service_cfg = service_config(service_name)
service_cfg['kwargs']['name'] = service_name

module = import_module('skyway.' + service_cfg['module'] + '.service')
service_class = getattr(module, 'Service')
service_instance = service_class(**(service_cfg['kwargs']))
update_run(service_name, pid=os.getpid(), status=status)
ts_now, ts_next, running = 1, 0, True

def on_exit(sid, frame):
    global running
    running = False
    
signal.signal(signal.SIGTERM, on_exit)

while running:
    ts_now = time()

    if ts_now > ts_next:
        ts_next = ts_now + service_cfg['every']

        if get_status(service_name)['status'] in ['running', 'testing']:
            service_instance()

        update_run(service_name)
    else:
        sleep(1)

del service_instance
update_run(service_name, pid=0, status='stopped')
logging.info('Service daemon stopped.')