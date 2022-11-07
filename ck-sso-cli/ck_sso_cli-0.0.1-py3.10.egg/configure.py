import sys 

def configure():
    profile = 'default'
    if len(sys.argv)==2:
        print('Using default profile')
    elif len(sys.argv)==4:
        if sys.argv[2]=='--profile':
            profile = sys.argv[3]
        else:
            print()

    print(profile)