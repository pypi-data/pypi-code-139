from .session import assume_role

def get_account_regions(accounts):
    account_regions = list(set([(a['account_id'], a['region']) for a in accounts]))
    return [{'account_id':a[0], 'region':a[1]} for a in account_regions]

def get_session(data, **kargs):
    reg = data.get('region')
    aid = data.get('account_id')
    ss = data.get('session')
    accounts = args.get('accounts')
    if not ss:
        ss = {}
        account_regions = get_account_regions(accounts)
        for a in account_regions: ss.update({aid:{}})
    s = ss.get(aid,{}).get(reg,None)
    if not s:
        try:     ss[aid][reg] = assume_role(access_key_id = args.get('access_key'), 
                                            secret_access_key = args.get('secret'), 
                                            roleName = args.get('role'), 
                                            accountId = aid, region=reg)
        except:  pass
    return {'accounts':accounts, 'session':ss}

def update_dataframe_with_func(**kargs):
    results = [run_func(a, **kargs) for a in accounts]
    return (results, data['session'])

def run_func(a, data, **kargs):
    account_id = a.get('account_id')
    region = a.get('region')
    kargs.update({'account_id':account_id, 'region':region})
    data = get_session(**kargs)
    s = data.get('session',{}).get(account_id,{}).get(region,None)
    if s:
        kargs.update({'session':s,'row':a})
        a.update({kargs.get('key'): kargs.get('func')(s, **kargs)})
        return a
    return None
