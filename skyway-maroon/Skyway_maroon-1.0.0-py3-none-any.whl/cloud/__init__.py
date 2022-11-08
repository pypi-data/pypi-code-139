from skyway import *
import yaml

class Cloud():
    
    @staticmethod
    def create(vendor, kwargs):
        vendor = vendor.lower()
        vendor_cfg = load_config('cloud')
        
        if vendor not in vendor_cfg:
            raise Exception('Cloud vendor [%s] is undefined.' % (vendor))
                
        from importlib import import_module
        module = import_module('skyway.cloud.' + vendor)
        cloud_class = getattr(module, vendor.upper())
        return cloud_class(vendor_cfg[vendor], kwargs)
    
    def __init__(self, vendor_cfg, kwargs):
        self.vendor = vendor_cfg
        
        for k, v in kwargs.items():
            setattr(self, k.replace('-','_'), v)
    
    def connect_node(self, hostname):
        print("Extract node information:", hostname)
        ip = self.get_host_ip(hostname)
        
        print("Connect to IP:", ip)
        cmd = 'ssh ' + self.vendor['username'] + '@' + ip
        os.system(cmd)