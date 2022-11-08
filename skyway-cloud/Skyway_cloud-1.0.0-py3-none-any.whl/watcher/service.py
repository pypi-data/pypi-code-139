from . import *
from skyway.service import *
import logging

class Service(ServiceBase):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info('Watcher service started.')
    
    def __call__(self, **kwargs):
        status_file = cfg['paths']['var'] + "watcher.yaml"
        
        if os.path.isfile(status_file):
            with open(status_file, 'r') as fp:
                status = yaml.load(fp, Loader=yaml.FullLoader)
        else:
            status = {}
        
        #print('old', status)
        new_status = {k:'unknown' for k in status}
        changes = []
        
        for service_name in services:
            if assert_run(service_name):                            
                if service_name not in status:
                    status[service_name] = 'unknown'
                    new_status[service_name] = 'unknown'
                
                pinfo = get_status(service_name)
                
                if pinfo['status'] != status[service_name]:
                    changes.append("%s: %s => %s" %(service_name, status[service_name], pinfo['status']))
                
                new_status[service_name] = pinfo['status']
                
        for k, v in new_status.items():
            if v == 'unknown':
                changes.append("%s: %s => unknown" %(k, status[k]))
                
        #print('new', new_status)
        
        with open(status_file, 'w') as fp:
            fp.write(yaml.dump(new_status))
        
        if changes != []:
            sendmail('skyway@rcc.uchicago.edu', "Skyway service status change", "\r\n\r\n".join(changes))
            
            for _ in changes:
                logging.info(_)
                
        
    
    def __del__(self):
        pass