from skyway import *
from datetime import datetime
import os, time
from time import sleep

service_path = cfg['paths']['etc'] + 'services/'
services = [file[:-5] for file in os.listdir(service_path) if file.endswith('.yaml')]

def assert_config(name):
    if name not in services:
        raise Exception('Service [%s] does not exist.' % (name))

def assert_run(name, strict=False):
    assert_config(name)
    
    if not os.path.isfile(cfg['paths']['run'] + name + '.yaml'):
        if strict:
            raise Exception('Service [%s] has not registration. Run --regist first.')
        else:
            return False
    
    return True

def get_run(name):
    assert_run(name, strict=True)
    
    with open(cfg['paths']['run'] + name + '.yaml', 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)

def check_service(pid, service_name):
    process_name = proc("ps -o cmd= " + str(pid), strict=False)
    return ['python3 -m skyway.service.daemon ' + service_name] == process_name
        
def get_status(name):
    pinfo = None
    
    while pinfo is None:
        pinfo = get_run(name)
        if pinfo is None: sleep(1)
    
    process_name = proc("ps -o cmd= " + str(pinfo['pid']), strict=False)
    
    if (pinfo['status'] not in ['testing', 'stopped']) and (check_service(pinfo['pid'], name) == False):
        pinfo['status'] = 'failed'
    
    return pinfo
    
def update_run(name, update=True, **kwargs):
    run_status = get_run(name) if update else {'pid': 0, 'status': 'stopped'}
    run_status.update(kwargs)
    run_status['update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(cfg['paths']['run'] + name + '.yaml', 'w') as fp:
        fp.write(yaml.dump(run_status))

def service_config(name):
    assert_config(name)
    
    with open(service_path + name + ".yaml", 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)


def start_service(service_name):
    assert_run(service_name)
    pinfo = get_status(service_name)

    if pinfo['status'] in ['running', 'paused']:
        print("Service is already running.")
        return

    outfile = cfg['paths']['run'] + service_name + '.run'
    proc("nohup skyway service.daemon %s > %s 2>&1 &" % (service_name, outfile))

def stop_service(service_name):
    assert_run(service_name)
    pinfo = get_status(service_name)

    if pinfo['status'] == 'running':
        proc('kill -9 ' + str(pinfo['pid']))
        
        while check_service(pinfo['pid'], service_name):
            time.sleep(1)
    else:
        print("Service is not running.")
            
class ServiceBase:
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        
