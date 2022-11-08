from . import *
import argparse

class AccountAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, 'billing', Billing(values[0]))        

class SummaryAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        usages = namespace.billing.usages()
        print("\n" + tabulate(usages['bills'], headers=['Usages', 'Hours', 'Cost($)']))
        print("\n" + tabulate(usages['rates'], headers=['Running', 'Count', 'Rate($/hr)']) + "\n")
        print("Budget:       $%0.3f (started from %s)" % (usages['budget']['amount'], usages['budget']['start']))
        print("Maximum Rate: $%0.3f/Hour" % (usages['budget']['rate']))
        print("Current Rate: $%0.3f/Hour" % (usages['rate']))
        print("Total Cost:   $%0.3f" % (usages['total']))
        print("Balance:      $%0.3f" % (usages['budget']['amount'] - usages['total']))
        print("Status:       %s\n" % (usages['status'].upper()))
        
class SetAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        w = [v.strip() for v in values[0].split('=')]
        namespace.billing.set(w[0], w[1])
        
parser = argparse.ArgumentParser(description='Manage Skyway cloud resources.')
group = parser.add_mutually_exclusive_group()

parser.add_argument('account', action=AccountAction, metavar='account', nargs=1, help='accout name')
group.add_argument('--summary', action=SummaryAction, nargs=0, help='list nodes')
group.add_argument('--set', action=SetAction, nargs=1, help='Set value by [key=value]')
args = parser.parse_args()
