def get_account_regions(accounts):
    account_regions = list(set([(a['account_id'], a['region']) for a in accounts]))
    return [{'account_id':a[0], 'region':a[1]} for a in account_regions]

def get_session(args):
    reg = args['region']
    aid = args['account_id']
    ss = args.get('session')
    if not ss:
        account_regions = get_account_regions(args.get('accounts'))
        ss = {}
        for a in account_regions: ss.update({a['account_id']:{}})
    s = ss.get(aid,{}).get(reg,None)
    if not s:
        try:
            ss[aid][reg]=ar(key,sec,aid,role,reg)
        except:
            pass
    return {'accounts':accounts, 'session':ss}

def update_dataframe_with_func(**kargs):
    data = {'accounts':kargs.get('cur'), 'session':kargs.get('session')}
    results = [run_func(a, data,**kargs) for a in data['accounts']]
    return (results, data['session'])

def run_func(a, data, **kargs):
    account_id = a['account_id']
    region = a['region']
    data.update({'account_id':account_id, 'region':region})
    data = get_session(data)
    s = data['session'].get(account_id,{}).get(region,None)
    if s:
        kargs.update({'session':s,'row':a})
        a.update({kargs.get('key'): kargs.get('func')(s, **kargs)})
        return a
    return None
