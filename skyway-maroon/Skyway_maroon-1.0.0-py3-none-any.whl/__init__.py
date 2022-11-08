
import yaml
from tabulate import tabulate
import os, sys
from subprocess import PIPE, Popen

if 'SKYWAYROOT' not in os.environ:
    raise Exception('SKYWAY_ROOT is not set in envrionment.')

cfg_path = os.environ['SKYWAYROOT'] + '/etc/'
debug = 'SKYWAYDEBUG' in os.environ

def load_config(cfg_name):
    cfg_file = cfg_path + cfg_name + '.yaml'
    
    if not os.path.isfile(cfg_file):
        raise Exception('Configuration file [%s.p] cannot be found.' % (cfg_name))
    
    with open(cfg_file, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)

cfg = load_config('skyway')

if os.getuid() == 0:
    cfg.update(load_config('root'))

for k in cfg['paths']:
    cfg['paths'][k] = cfg['paths'][k].replace('<ROOT>', os.environ['SKYWAYROOT'])

def proc(command, strict = True):
    
    if isinstance(command, list):
        command = ' '.join(command)

    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    out = stdout.decode('ascii').strip()
    err = stderr.decode('utf-8').strip()
    
    if strict and err !="":
        raise Exception('Shell error: ' + err + '\nCommand: ' + command)
    
    if out == "": return []
    else: return out.split('\n')

def sendmail(to, subject, body):
    mail = "\r\n".join([
        'From: ' + cfg['email'],
        'To: ' + to,
        'Subject: ' + subject,
        '',
        body
    ])
    
    proc("echo \"" + mail + "\" | sendmail -v '" + to + "'")

from .nodemap import NodeMap
NodeMap.lock_file = cfg['paths']['var'] + 'nodes.lock'

def get_username(uid):
    uid = proc("getent passwd " + uid + " | awk -F: '{print $1}'")
    return None if uid==[]  else uid[0]
    
