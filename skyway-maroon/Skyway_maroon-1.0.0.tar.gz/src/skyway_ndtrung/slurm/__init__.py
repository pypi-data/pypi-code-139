from skyway import *
import skyway.account as account
import time
    
class slurm:
    
    @staticmethod
    def ts2secs(ts):
        ts = ts.split('-')
        if len(ts)==1:
            days = 0
            hms = ts[0]
        else:
            days = int(ts[0])
            hms = ts[1]
        
        hms = hms.split(':')
        if len(hms) == 1:
            hms = ['0', '0'] + hms[0:1]
        elif len(hms) == 2:
            hms = ['0'] + hms[0:2]
        
        return days * 86400 + int(hms[0]) * 3600 + int(hms[1]) * 60 + int(hms[2])
    
    @staticmethod
    def sacctmgr(args):
        return proc(['sacctmgr -i'] + args)
                
    @staticmethod
    def assoc_list():
        
        assocs = []
        rows = slurm.sacctmgr(['-n -p list assoc format=account,user'])
        
        for row in rows:
            w = row.split('|')
            if w[1]=='root' or w[1] == '': continue
            assocs.append(w[:-1])

        return assocs
    
    @staticmethod
    def account_users():
        u = {acct:[] for acct in slurm.accounts()}
        
        for row in slurm.assoc_list():
            if row[0] not in u:
                u[row[0]] = []
            
            u[row[0]].append(row[1])
        
        return u
        
    @staticmethod
    def add_assoc(acct, user):

        slurm.sacctmgr(['add user', user, 'account=' + acct, 'partition=' + acct])
        return
    
    @staticmethod
    def del_assoc(acct, user):
        
        assoc_users = {}
        
        for assoc in slurm.assoc_list():
            if assoc[1] not in assoc_users:
                assoc_users[assoc[1]] = 1
            else:
                assoc_users[assoc[1]] += 1
        
        if user in assoc_users and assoc_users[user]>1:
            slurm.sacctmgr(['remove user', user, 'where account=' + acct])
        else:
            slurm.sacctmgr(['remove user', user])
            
        return
    
    @staticmethod
    def accounts():

        accts = []

        for row in slurm.sacctmgr(['-n list account format=account%-64']):
            acct = row.strip()
            if acct != 'root': accts.append(acct)

        return accts
    
    @staticmethod
    def node_status(partition, feature):

        status = { "drain" : [], "idle" : [], "down": [] }

        for row in proc(['sinfo -h -p', partition, '--format=%t,%n,%f']):
            w = row.split(",")
            if w[2] != feature: continue
            state = w[0].replace('*', '')
            name = w[1]
            if state in status: status[state].append(name)

        return status
    
    @staticmethod
    def show_node(nodename):

        node = {}

        for row in proc(['scontrol show node', nodename]):
            words = row.split()
            for word in words:
                w = word.split('=')
                if len(w)<2 : continue
                node[w[0]] = w[1]

        return node
    
    @staticmethod
    def partition_jobs(partition):
        jobs = proc(['squeue -h -p', partition, '--format=%A'])
        return jobs if jobs != [""] else []
    
    @staticmethod
    def running_jobs(partition):
        jobs = proc(['squeue -h -t R -p', partition, '--format=%A,%u,%f,%M,%l,%L'])
        return [job.split(',') for job in jobs] if jobs != [""] else []
    
    @staticmethod
    def usage_nodetime(partition, user=None):
        cmd = 'sacct -XPn --partition=%s %s --starttime=2018-01-01T00:00:00 --format=NodeList,ElapsedRaw' % (partition, "" if user is None else " --user="+user)
        
        total = {}
        for one in [one.split('|') for one in proc([cmd])]:
            if one[1] != '0':
                mt = one[0].split('-')[2]
                
                if mt not in total:
                    total[mt] = 0.0
                
                total[mt] += float(one[1]) / 3600
        
        return total
        
        
    
    @staticmethod
    def cancel_jobs(jobs):
        proc(['scancel', ",".join(jobs)], strict=False)
        
    @staticmethod
    def pending_jobs_count(partition, feature):

        z = proc(['squeue -h -p', partition, '-t PD --format=%f,%D,%u,%r | grep -v Depend '])
        n = 0

        for row in z:
            w = row.split(',')
            if w[0] == feature: n = n + int(w[1])

        return n
        
    @staticmethod
    def reconfigure():

        proc(['scontrol reconfig'])
        return
    
    @staticmethod
    def update_node_state(node, state, reason="idle"):

        changed = 'state=' + state
        if state == 'drain': changed += ' reason=' + reason
        proc(['scontrol update node=' + node, changed])
        return
    
    @staticmethod
    def get_usages(args):

        fmt = "--format=User,NNodes,ElapsedRaw,NodeList"
        begin = "--starttime=2018-10-01T00:00:00"
        opt = '-a '

        for arg in args:
            opt += '--' + arg + '=' + args[arg]

        jobs = proc(['sacct -n -X -P', opt, begin, fmt, '| grep -v "None assigned"'])

        total = {}

        for job in jobs:
            user, nnodes, elapsed, nodelist = job.split('|')

            nodetype = (':').join(nodelist.split('-')[0:4])
            if '.' in nodetype: continue
            if nodetype == "": continue

            label = user + ":" + nodetype
            job_hours = float(elapsed) / 3600
            node_hours = int(float(elapsed) / 3600) + 1

            if label not in total:
                total[label] = [0, 0]

            total[label][0] += job_hours * int(nnodes)
            total[label][1] += node_hours * int(nnodes)

        return total
    
    @staticmethod
    def get_defaccount(u):
        return proc(['sacctmgr -nP show user where user=%s format=defaultaccount' % (u)])[0]


