from . import *
from ..slurm import slurm
import os, sys

account, outdir = sys.argv[1], sys.argv[2]
bill = Billing(account)
usages = bill.usages()

output = ["\n" + tabulate(usages['bills'], headers=['Usages', 'Hours', 'Cost($)']), "",
    tabulate(usages['rates'], headers=['Running', 'Count', 'Rate($/hr)']), "",
    "Budget:       $%0.3f (started from %s)" % (usages['budget']['amount'], usages['budget']['start']),
    "Maximum Rate: $%0.3f/Hour" % (usages['budget']['rate']),
    "Current Rate: $%0.3f/Hour" % (usages['rate']),
    "Total Cost:   $%0.3f" % (usages['total']),
    "Balance:      $%0.3f" % (usages['budget']['amount'] - usages['total']),
    "Status:       %s\n" % (usages['status'].upper()), ""
]

with open(outdir + "/group-summary", "w") as f:
    f.write("\n".join(output))



puquota_file = '/skyway/misc/' + account + '.quota.yaml'
if os.path.isfile(puquota_file):
    users = []
    import yaml
    
    try:
        userquota = yaml.load(open(puquota_file), Loader=yaml.FullLoader)
    except:
        print("Incorrect format of quota file.")
        exit()
    
    for user, quota in userquota.items():
        usage = bill.user_usages(user)
        users.append([user, quota, usage[0], quota - usage[0]])
    
output = "\n" + tabulate(users, headers=['User', 'Quota', 'Usage', 'Balance']) + "\n\n"

with open(outdir + "/group-users", "w") as f:
    f.write(output)