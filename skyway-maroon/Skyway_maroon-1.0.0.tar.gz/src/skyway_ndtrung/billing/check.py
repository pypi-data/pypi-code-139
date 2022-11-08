from . import *
from ..slurm import slurm

if False: # accept all jobs 
    print('***JOB ACCEPTED***'); exit()

if False: # deny all jobs
    print('***Service is not available.***'); exit()

# Regular process

import argparse
parser = argparse.ArgumentParser(description='Skyway billing checker.')

for arg in ['account', 'user', 'partition', 'qos', 'feature', 'setting', 'time']:
    parser.add_argument('-' + arg[0], '--' + arg, default='', type=str)

args = parser.parse_args()
args.user = get_username(args.user)
args.time = int(args.time) / 60
bill = Billing(args.account)

# Check job usage

tasks, nodes, tpn = args.setting.split(',')

if int(nodes)>1:
    print("Incorrect setting: --setting=" + args.setting)
    print("Error: incorrect number of nodes for the job (should use --nodes=1)")
    exit()

usages = bill.usages()
nodetypes = bill.cloud_cfg['node-types']
nodetype = nodetypes[args.feature]
est_cost = args.time * nodetype['price']

running = slurm.running_jobs(args.account)
running_cost = sum([nodetypes[job[2]]['price'] * slurm.ts2secs(job[5]) / 3600 for job in running])
check = '***JOB ACCEPTED***'

output = ["",
    "Skyway billing checking for group account ...", "",
    "Cloud Account:   " + args.account,
    "Cloud Vendor:    " + bill.cloud,
    "Running Cost:    $%0.3f" % (running_cost),
    "Requested Node:  %s (%s)" % (args.feature, nodetype['name']),
    "Node Unit Price: $%0.3f/hour" % (nodetype['price']),
    "Requested Time:  %0.3f-hour" % (args.time),
    "Estimated Cost:  $%0.3f" % (est_cost),
    ""
]
    
# Check user balance

puquota_file = '/skyway/misc/' + args.account + '.quota.yaml'

if os.path.isfile(puquota_file):
    import yaml
    
    try:
        userquota = yaml.load(open(puquota_file), Loader=yaml.FullLoader)
    except:
        print("Incorrect format of quota file.")
        exit()
    
    if args.user not in userquota:
        print("User-quota is not specified.")
        exit()
    
    my_quota = userquota[args.user]
    my_usages = bill.user_usages(args.user)
    est_balance = my_quota - my_usages[0] - est_cost
    
    output += [
        "User Budget: %s" % my_quota,
        "User Estimated Balance: $%0.3f" % est_balance,
        ""
    ]
    
    if est_balance<0:
        check = '***JOB REJECTED***'

# Check group balance

est_balance = usages['balance'] - est_cost - running_cost

if est_balance<0:
    check = '***JOB REJECTED***'

output += [
    "Group Budget:   $%0.3f (from %s)" % (bill.budget['amount'], bill.budget['start']),
    "Group Usage:    $%0.3f" % (usages['total']),
    "Group Balance:  $%0.3f" % (usages['balance']),
    "Group Estimated Balance: $%0.3f" % (est_balance),
    "", check, ""
]

print("\n".join(output))
