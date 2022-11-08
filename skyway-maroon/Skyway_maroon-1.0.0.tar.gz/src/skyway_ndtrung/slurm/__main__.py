from . import *


if len(sys.argv)<2:
    print('''
Usage:

  --update-users    update accounts and users in SLURMDBD
  --update-conf     update slurm.conf (needs to restart slurmctld manually)
  
    ''')

elif sys.argv[1] == '--update-users':
    slurm_users = slurm.account_users()
    skyway_accts = account.accounts()
    
    # Sync users to slurm
    
    for acct in skyway_accts:
        if acct not in slurm_users:
            raise Exception("No SLURM account %s. Do the following action first:\nsacctmgr add account %s" % (acct, acct))
        
        skyway_users = account.load_cfg(acct)['users']
        
        for u in skyway_users:
            if u not in slurm_users[acct]:
                print("Add user %s to account %s" % (u, acct))
                slurm.add_assoc(acct, u)
        
        for u in slurm_users[acct]:
            if u not in skyway_users:
                print("Remove user %s from account %s" % (u, acct))
                slurm.del_assoc(acct, u)
    
    # Clean deactivated accounts
    
    for acct in slurm_users:
        if acct not in skyway_accts and len(slurm_users[acct])>0:
            print("Empty account " + acct)
            
            for u in slurm_users[acct]:
                print("Remove user %s from account %s" % (u, acct))
                slurm.del_assoc(acct, u)

elif sys.argv[1] == '--update-conf':
    hosts = []
    nodes = []
    parts = []
    gres =  []
    
    for acct in account.accounts():
        partnodes = []
        group, cloud = acct.split('-')
        nt_cfg = load_config('cloud')[cloud]['node-types']
        
        for nodetype, count in account.load_cfg(acct)['nodes'].items():
            node_cfg = nt_cfg[nodetype]
            print("Node Def:", node_cfg)
            
            cores = node_cfg['cores']
            memmb = node_cfg['memgb'] * 1000 * 0.9
            extra = ""
            
            typename = "%s-%s" % (acct, nodetype)
            nodelist = ('%s-[%03d-%03d]' % (typename, 1, count)) if count>1 else ('%s-001' % (typename))
            partnodes.append(nodelist)
            
            hosts += ["%s-%03d" % (typename, i+1) for i in range(count)]
            
            if 'gpu' in node_cfg: 
                extra = "Gres=gpu:" + str(node_cfg['gpu'])

                if node_cfg['gpu'] == 1: devs = "0"
                else: devs = "[0-%d]" % (node_cfg['gpu']-1)
                
                gres.append("NodeName=%s Name=gpu File=/dev/nvidia%s" % (nodelist, devs))
            
            nodes.append("NodeName=%s CoresPerSocket=%d RealMemory=%d Feature=%s %s" %
                        (nodelist, cores, memmb, nodetype, extra))
            
        parts.append("PartitionName=%s Nodes=%s" % (acct, ",".join(partnodes)))
    
    NodeMap().rebuild(hosts).dump_hosts()
    
    with open(cfg['paths']['var'] + 'slurm.conf-base', 'r') as f:
        conf_base = f.read()
    
    with open('/skyway/files/etc/slurm/slurm.conf', 'w') as f:
        f.write(conf_base + '\n'.join(nodes) + '\n\n' + '\n'.join(parts))
        
    with open('/skyway/files/etc/slurm/gres.conf', 'w') as f:
        f.write('\n'.join(gres))
    
else:
    print("Error: unknown command!")

        
        
        
        
    
