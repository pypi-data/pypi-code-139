from skyway import *
from ..cloud import *
from ..slurm import slurm
import skyway.account as account
from skyway.db import DBConnector 
from skyway.nodemap import NodeMap
import os

class Billing:
    
    def __init__(self, account_name):
        self.account = account_name
        budget_cols = 'cloud,startdate,amount,rate'
        budget_row = DBConnector().select('budget', budget_cols, where="account='%s'" % (account_name), limit='1')[0]
        self.cloud = budget_row[0]
        
        self.budget = {
            'start': str(budget_row[1]),
            'amount': budget_row[2],
            'rate': budget_row[3]
        }
        
        billing_file = cfg['paths']['var'] + 'billing/' + account_name + '.yaml'

        if os.path.isfile(billing_file):
            with open(billing_file, 'r') as f:
                for k,v in yaml.load(f, Loader=yaml.FullLoader).items():
                    if k in ['status']:
                        setattr(self, k, v)
        
        self.cloud_cfg = load_config('cloud')[self.cloud]
    
    def usages(self):
        nt = self.cloud_cfg['node-types']
        bills = [[t+":"+nt[t]['name'], h, nt[t]['price'] * h] for t,h in NodeMap.history_summary(self.account, self.budget['start']).items()]
        rates = [[t+":"+nt[t]['name'], n, nt[t]['price'] * n] for t,n in NodeMap.running_summary(self.account).items()]
        total = sum([bill[-1] for bill in bills])
        pct = total * 100 / self.budget['amount']
        
        return {
            'cloud': self.cloud,
            'bills': bills,
            'rates': rates,
            'total': total,
            'rate': sum([rate[-1] for rate in rates]),
            'budget': self.budget,
            'balance': self.budget['amount'] - total,
            'pct': pct,
            'status': 'normal' if pct<90 else ('warning' if pct<100 else 'exceeded')
        }
    
    def user_usages(self, user):
        nt = self.cloud_cfg['node-types']
        usages, total = {}, 0.0
        
        for t,h in slurm.usage_nodetime(self.account, user).items():
            ex = h * nt[t]['price']
            usages[t] = [nt[t]['price'], h, ex]
            total += ex
        
        return total, usages
    
    def set(self, key, value):
        DBConnector().update_one('budget', 'account', self.account, {key:value})
        
    
