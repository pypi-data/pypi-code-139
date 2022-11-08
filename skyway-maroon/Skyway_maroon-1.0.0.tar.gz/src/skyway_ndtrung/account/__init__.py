from skyway import *

def accounts():
    return sorted([f.split('.')[0] for f in os.listdir(cfg['paths']['etc'] + '/accounts') if f.endswith('.yaml')])

def load_cfg(account):
    global cfg
    
    if account not in accounts():
        raise Exception('Account [%s] does not exist.' % (account))
    
    cfg_file = "%s/accounts/%s.yaml" % (cfg['paths']['etc'], account)
    with open(cfg_file, "r") as f:
        acct_cfg = yaml.load(f, Loader=yaml.FullLoader)
    
    return acct_cfg
