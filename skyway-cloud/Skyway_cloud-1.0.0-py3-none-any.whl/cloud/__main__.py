from . import *
import skyway.account as account
from tabulate import tabulate
import argparse

class AccountAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        cfg = account.load_cfg(values[0])
        setattr(namespace, 'account', values[0])
        setattr(namespace, 'config', cfg)
        setattr(namespace, 'cloud', Cloud.create(cfg['cloud'], cfg['account']))
        

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        nodes = namespace.cloud.list_nodes()
        nmap = {v['instance']:k for k, v in NodeMap().nodes.items() if v['instance']!=''}
        nmap = {}
        for node in nodes:
            node.append(nmap[node[3]] if node[3] in nmap else '-')
        
        nodes.sort(key=lambda x: x[4])
        print("\nNodes for account [%s]:\n" % (namespace.account))
        print(tabulate(nodes, headers=['Name', 'Status', 'Type', 'Instance ID', 'Host']))
        print("")
        
class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        nmap = NodeMap()
        nmap.power_off(cloud=namespace.config['cloud'], instance=values[0])
        nmap.dump_hosts()
        namespace.cloud.destroy_nodes(values)

class CreateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        namespace.cloud.create_nodes(values, ['test'])
        
class ConnectAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        namespace.cloud.connect_node(values[0])
        
class TestAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        print(dir(namespace.cloud))

parser = argparse.ArgumentParser(description='Manage Skyway cloud resources.')
group = parser.add_mutually_exclusive_group()

parser.add_argument('account', action=AccountAction, metavar='account', nargs=1, help='accout name')
group.add_argument('--ls', action=ListAction, nargs=0, help='list nodes')
group.add_argument('--rm', action=RemoveAction, nargs=1, metavar='node', help='terminate nodes')
group.add_argument('--cr', action=CreateAction, metavar='type', help='testing creation of a node')
group.add_argument('--connect', action=ConnectAction, nargs=1, metavar='node', help='connect to a node')
group.add_argument('--test', action=TestAction, nargs=0, metavar='node', help='test a cloud account')
args = parser.parse_args()
