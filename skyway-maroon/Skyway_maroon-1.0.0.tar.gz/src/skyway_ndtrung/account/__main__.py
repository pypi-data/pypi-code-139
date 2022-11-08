from . import *

def update_pam():
    users = []
    
    for acct in accounts():
        users += load_cfg(acct)['users']
    
    nerror = 0
    
    for u in set(users):
        if proc('getent passwd ' + u) == []:
            print('Unknown user: ' + u)
            nerror += 1
    
    if nerror>0:
        raise Exception('Unknown user(s) found!')

    passwd_ext = "\n".join(proc('getent passwd '+ u)[0] for u in set(users))
    group_ext  = "\n".join(proc('getent group  '+ u)[0] for u in set(users))
    shadow_ext = "\n".join(proc('getent shadow '+ u)[0] for u in set(users))
    
    with open(cfg['paths']['var'] + 'passwd', 'r') as f:
        rows = f.read().strip()
    
    with open("/skyway/files/etc/passwd", "w") as f:
        f.write(rows + "\n" + passwd_ext + "\n")
    
    with open(cfg['paths']['var'] + 'group', 'r') as f:
        rows = f.read().strip()
    
    with open("/skyway/files/etc/group", "w") as f:
        f.write(rows + "\n" + group_ext + "\n")
    
    with open(cfg['paths']['var'] + 'shadow', 'r') as f:
        rows = f.read().strip()
    
    with open("/skyway/files/etc/shadow", "w") as f:
        f.write(rows + "\n" + shadow_ext + "\n")




if len(sys.argv)<2 or sys.argv[1]=='--list':
    print("\nAccounts:\n\n" + yaml.dump(accounts()))

elif sys.argv[1] == '--update':
    update_pam()
    
elif len(sys.argv)>2 and sys.argv[1] == '--show':
    acct = sys.argv[2]
    print("\nAccount " + acct + ":\n\n" + yaml.dump(load_cfg(acct)))

else:
    print("Syntax error! " + str(sys.argv[1:]))
