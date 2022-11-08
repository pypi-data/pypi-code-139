from . import *
from skyway.account import accounts
from skyway.service import ServiceBase
import logging

class Service(ServiceBase):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info('Bill service started.')
    
    def __call__(self, **kwargs):
        for account in accounts():
            bill = Billing(account)
            usages = bill.usages()
            
            if hasattr(bill, 'status') and usages['status'] != bill.status:
                message = 'Skyway account ' + account + ' budget ' + usages['status']                
                sendmail('skyway@rcc.uchicago.edu', message, yaml.dump(usages))
                logging.info(message)
            
            with open(cfg['paths']['var'] + 'billing/' + account + '.yaml', 'w') as f:
                f.write(yaml.dump(usages))
    
    def __del__(self):
        pass